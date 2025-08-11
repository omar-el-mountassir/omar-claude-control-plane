#!/usr/bin/env python3
"""
PADA GitHub Monitor - Personal Development Repository Monitoring
Monitors Omar's GitHub repositories for development workflow events
"""

import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import json

# Import PADA core types
from .pada_main import Event

logger = logging.getLogger(__name__)

@dataclass
class GitHubRepository:
    """GitHub repository configuration"""
    owner: str
    name: str
    full_name: str
    monitored_events: List[str]
    priority: str  # HIGH, MEDIUM, LOW
    last_checked: datetime

class GitHubMonitor:
    """Monitor GitHub repositories for development workflow events"""
    
    def __init__(self, github_config: Dict[str, Any]):
        self.config = github_config
        self.api_token = github_config.get('token')
        self.base_url = 'https://api.github.com'
        self.repositories = []
        self.session: Optional[aiohttp.ClientSession] = None
        self.is_running = False
        self.last_poll_time = {}
        
        # Initialize repositories from config
        self._load_repositories()
        
        logger.info(f"GitHub Monitor initialized for {len(self.repositories)} repositories")
    
    def _load_repositories(self):
        """Load repository list from config"""
        repo_configs = self.config.get('repositories', [])
        
        for repo_config in repo_configs:
            repo = GitHubRepository(
                owner=repo_config['owner'],
                name=repo_config['name'], 
                full_name=f"{repo_config['owner']}/{repo_config['name']}",
                monitored_events=repo_config.get('events', [
                    'push', 'pull_request', 'issues', 'workflow_run', 'security_alert'
                ]),
                priority=repo_config.get('priority', 'MEDIUM'),
                last_checked=datetime.utcnow() - timedelta(hours=1)
            )
            self.repositories.append(repo)
            self.last_poll_time[repo.full_name] = repo.last_checked
    
    async def start(self):
        """Start GitHub monitoring"""
        logger.info("Starting GitHub monitor...")
        
        # Create HTTP session with authentication
        headers = {}
        if self.api_token:
            headers['Authorization'] = f'Bearer {self.api_token}'
            headers['Accept'] = 'application/vnd.github.v3+json'
        
        connector = aiohttp.TCPConnector(limit_per_host=5)
        self.session = aiohttp.ClientSession(
            headers=headers,
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        
        self.is_running = True
        logger.info("GitHub monitor started")
    
    async def stop(self):
        """Stop GitHub monitoring"""
        logger.info("Stopping GitHub monitor...")
        
        self.is_running = False
        
        if self.session:
            await self.session.close()
        
        logger.info("GitHub monitor stopped")
    
    async def get_new_events(self) -> List[Event]:
        """Get new events from all monitored repositories"""
        
        if not self.session:
            logger.warning("GitHub monitor not started")
            return []
        
        all_events = []
        
        for repo in self.repositories:
            try:
                repo_events = await self._get_repository_events(repo)
                all_events.extend(repo_events)
            except Exception as e:
                logger.error(f"Error getting events for {repo.full_name}: {e}")
        
        logger.info(f"Retrieved {len(all_events)} new GitHub events")
        return all_events
    
    async def _get_repository_events(self, repo: GitHubRepository) -> List[Event]:
        """Get events for a specific repository"""
        
        events = []
        since_time = self.last_poll_time.get(repo.full_name, datetime.utcnow() - timedelta(hours=1))
        
        # Get different types of events based on configuration
        for event_type in repo.monitored_events:
            try:
                if event_type == 'push':
                    events.extend(await self._get_push_events(repo, since_time))
                elif event_type == 'pull_request':
                    events.extend(await self._get_pr_events(repo, since_time))
                elif event_type == 'issues':
                    events.extend(await self._get_issue_events(repo, since_time))
                elif event_type == 'workflow_run':
                    events.extend(await self._get_workflow_events(repo, since_time))
                elif event_type == 'security_alert':
                    events.extend(await self._get_security_events(repo, since_time))
            except Exception as e:
                logger.error(f"Error getting {event_type} events for {repo.full_name}: {e}")
        
        # Update last poll time
        self.last_poll_time[repo.full_name] = datetime.utcnow()
        
        return events
    
    async def _get_push_events(self, repo: GitHubRepository, since: datetime) -> List[Event]:
        """Get push events that might need attention"""
        events = []
        
        # Get recent commits
        url = f"{self.base_url}/repos/{repo.full_name}/commits"
        params = {
            'since': since.isoformat() + 'Z',
            'per_page': 10
        }
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                commits = await response.json()
                
                for commit in commits:
                    # Look for potentially problematic commits
                    commit_msg = commit['commit']['message'].lower()
                    
                    is_important = any(keyword in commit_msg for keyword in [
                        'fix', 'bug', 'error', 'crash', 'security', 'urgent', 'hotfix'
                    ])
                    
                    if is_important:
                        event = Event(
                            id=f"push_{commit['sha'][:8]}",
                            source="github",
                            type="push_important",
                            title=f"Important commit in {repo.name}",
                            description=f"Commit: {commit['commit']['message'][:100]}",
                            severity="IMPORTANT" if any(word in commit_msg for word in ['security', 'urgent', 'hotfix']) else "HELPFUL",
                            timestamp=datetime.fromisoformat(commit['commit']['author']['date'].replace('Z', '+00:00')),
                            data={
                                'repository': repo.full_name,
                                'commit_sha': commit['sha'],
                                'commit_message': commit['commit']['message'],
                                'author': commit['commit']['author']['name'],
                                'url': commit['html_url']
                            },
                            requires_action=False,
                            suggested_actions=[]
                        )
                        events.append(event)
        
        return events
    
    async def _get_pr_events(self, repo: GitHubRepository, since: datetime) -> List[Event]:
        """Get pull request events requiring attention"""
        events = []
        
        # Get recent PRs
        url = f"{self.base_url}/repos/{repo.full_name}/pulls"
        params = {
            'state': 'open',
            'sort': 'updated',
            'per_page': 20
        }
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                prs = await response.json()
                
                for pr in prs:
                    updated_at = datetime.fromisoformat(pr['updated_at'].replace('Z', '+00:00'))
                    
                    if updated_at > since:
                        # Check if PR needs attention
                        requires_action = False
                        suggested_actions = []
                        severity = "HELPFUL"
                        
                        # PR ready for merge
                        if pr.get('mergeable') and not pr.get('draft'):
                            # Check if it's a safe merge candidate
                            pr_title = pr['title'].lower()
                            if any(safe_word in pr_title for safe_word in [
                                'typo', 'readme', 'docs', 'comment', 'test'
                            ]):
                                requires_action = True
                                suggested_actions = ['merge_safe_pr']
                                severity = "IMPORTANT"
                        
                        # PR has conflicts
                        elif pr.get('mergeable') is False:
                            severity = "IMPORTANT"
                            suggested_actions = ['rebase_branch']
                        
                        event = Event(
                            id=f"pr_{pr['number']}_{int(updated_at.timestamp())}",
                            source="github",
                            type="pull_request",
                            title=f"PR #{pr['number']}: {pr['title']}",
                            description=f"PR in {repo.name} updated: {pr['title'][:100]}",
                            severity=severity,
                            timestamp=updated_at,
                            data={
                                'repository': repo.full_name,
                                'pr_number': pr['number'],
                                'pr_title': pr['title'],
                                'author': pr['user']['login'],
                                'mergeable': pr.get('mergeable'),
                                'draft': pr.get('draft'),
                                'url': pr['html_url']
                            },
                            requires_action=requires_action,
                            suggested_actions=suggested_actions
                        )
                        events.append(event)
        
        return events
    
    async def _get_workflow_events(self, repo: GitHubRepository, since: datetime) -> List[Event]:
        """Get GitHub Actions workflow failures"""
        events = []
        
        # Get recent workflow runs
        url = f"{self.base_url}/repos/{repo.full_name}/actions/runs"
        params = {
            'status': 'failure',
            'per_page': 10
        }
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                runs = await response.json()
                
                for run in runs.get('workflow_runs', []):
                    updated_at = datetime.fromisoformat(run['updated_at'].replace('Z', '+00:00'))
                    
                    if updated_at > since:
                        # Workflow failure - always important
                        event = Event(
                            id=f"workflow_{run['id']}",
                            source="github",
                            type="workflow_failure",
                            title=f"Workflow failed: {run['name']}",
                            description=f"GitHub Actions workflow '{run['name']}' failed in {repo.name}",
                            severity="CRITICAL",
                            timestamp=updated_at,
                            data={
                                'repository': repo.full_name,
                                'workflow_name': run['name'],
                                'run_id': run['id'],
                                'conclusion': run['conclusion'],
                                'branch': run['head_branch'],
                                'url': run['html_url']
                            },
                            requires_action=True,
                            suggested_actions=['fix_linting', 'rebase_branch']
                        )
                        events.append(event)
        
        return events
    
    async def _get_issue_events(self, repo: GitHubRepository, since: datetime) -> List[Event]:
        """Get important issue updates"""
        events = []
        
        # Get recent issues
        url = f"{self.base_url}/repos/{repo.full_name}/issues"
        params = {
            'state': 'open',
            'sort': 'updated',
            'per_page': 10
        }
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                issues = await response.json()
                
                for issue in issues:
                    # Skip pull requests (GitHub API returns PRs as issues)
                    if 'pull_request' in issue:
                        continue
                    
                    updated_at = datetime.fromisoformat(issue['updated_at'].replace('Z', '+00:00'))
                    
                    if updated_at > since:
                        # Check severity based on labels
                        severity = "HELPFUL"
                        labels = [label['name'].lower() for label in issue.get('labels', [])]
                        
                        if any(label in ['bug', 'critical', 'urgent', 'security'] for label in labels):
                            severity = "CRITICAL"
                        elif any(label in ['enhancement', 'feature'] for label in labels):
                            severity = "IMPORTANT"
                        
                        event = Event(
                            id=f"issue_{issue['number']}_{int(updated_at.timestamp())}",
                            source="github",
                            type="issue_update",
                            title=f"Issue #{issue['number']}: {issue['title']}",
                            description=f"Issue updated in {repo.name}: {issue['title'][:100]}",
                            severity=severity,
                            timestamp=updated_at,
                            data={
                                'repository': repo.full_name,
                                'issue_number': issue['number'],
                                'issue_title': issue['title'],
                                'labels': labels,
                                'author': issue['user']['login'],
                                'url': issue['html_url']
                            },
                            requires_action=False,
                            suggested_actions=[]
                        )
                        events.append(event)
        
        return events
    
    async def _get_security_events(self, repo: GitHubRepository, since: datetime) -> List[Event]:
        """Get security alerts (requires appropriate GitHub permissions)"""
        events = []
        
        # Note: This endpoint requires security events permissions
        url = f"{self.base_url}/repos/{repo.full_name}/vulnerability-alerts"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    # Security alerts are always critical
                    event = Event(
                        id=f"security_{repo.full_name}_{int(datetime.utcnow().timestamp())}",
                        source="github",
                        type="security_alert",
                        title=f"Security alerts in {repo.name}",
                        description=f"Dependabot security alerts detected in {repo.name}",
                        severity="CRITICAL",
                        timestamp=datetime.utcnow(),
                        data={
                            'repository': repo.full_name,
                            'url': f"https://github.com/{repo.full_name}/security"
                        },
                        requires_action=True,
                        suggested_actions=['update_dependencies']
                    )
                    events.append(event)
                elif response.status != 404:  # 404 means no alerts
                    logger.warning(f"Could not access security alerts for {repo.full_name}: {response.status}")
        except Exception as e:
            logger.debug(f"Security alerts not available for {repo.full_name}: {e}")
        
        return events
    
    async def health_check(self) -> bool:
        """Check GitHub monitor health"""
        
        if not self.session:
            return False
        
        try:
            # Test API connectivity
            url = f"{self.base_url}/rate_limit"
            async with self.session.get(url) as response:
                if response.status == 200:
                    rate_limit_data = await response.json()
                    remaining = rate_limit_data['rate']['remaining']
                    
                    if remaining < 100:
                        logger.warning(f"GitHub API rate limit low: {remaining} requests remaining")
                    
                    return True
                else:
                    logger.error(f"GitHub API health check failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"GitHub monitor health check failed: {e}")
            return False

# Example configuration for testing
async def test_github_monitor():
    """Test GitHub monitor functionality"""
    
    print("🐙 Testing PADA GitHub Monitor")
    print("=" * 50)
    
    # Test configuration
    test_config = {
        'token': None,  # Add your GitHub token here for testing
        'repositories': [
            {
                'owner': 'anthropics',
                'name': 'claude-code',
                'events': ['push', 'pull_request', 'workflow_run'],
                'priority': 'HIGH'
            }
        ]
    }
    
    # Initialize monitor
    monitor = GitHubMonitor(test_config)
    
    try:
        # Start monitoring
        await monitor.start()
        
        # Health check
        health = await monitor.health_check()
        print(f"🏥 Health check: {'✅ Healthy' if health else '❌ Issues'}")
        
        if health:
            # Get events
            events = await monitor.get_new_events()
            print(f"📅 Found {len(events)} recent events")
            
            for event in events[:3]:  # Show first 3 events
                print(f"   • {event.type}: {event.title}")
        
        # Stop monitoring
        await monitor.stop()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        await monitor.stop()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_github_monitor())