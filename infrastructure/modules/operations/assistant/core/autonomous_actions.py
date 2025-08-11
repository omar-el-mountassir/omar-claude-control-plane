#!/usr/bin/env python3
"""
PADA Autonomous Actions - Safe AI-Driven Development Actions
Implements autonomous actions with comprehensive safety guardrails and validation
"""

import asyncio
import subprocess
import json
import logging
import aiohttp
import aiofiles
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import shutil
import tempfile

logger = logging.getLogger(__name__)

class ActionResult:
    """Result of executing an autonomous action"""
    
    def __init__(self, success: bool, details: Dict[str, Any] = None, error: str = None):
        self.success = success
        self.details = details or {}
        self.error = error
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'details': self.details,
            'error': self.error,
            'timestamp': self.timestamp.isoformat()
        }

class BaseAction:
    """Base class for all autonomous actions"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.execution_count = 0
        self.last_execution = None
        self.success_rate = 0.0
    
    async def execute(self, data: Dict[str, Any]) -> ActionResult:
        """Execute this action with given data"""
        raise NotImplementedError
    
    def is_safe(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if this action is safe to execute"""
        return True, "Safe"
    
    def get_requirements(self) -> List[str]:
        """Get list of requirements for this action to work"""
        return []
    
    async def dry_run(self, data: Dict[str, Any]) -> ActionResult:
        """Perform a dry run of this action"""
        return ActionResult(True, {"dry_run": True, "would_execute": True})

class GitHubAction(BaseAction):
    """Base class for GitHub-related actions"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.github_token = config.get('github_token')
        self.session = None
    
    async def _ensure_session(self):
        """Ensure HTTP session for GitHub API"""
        if not self.session:
            headers = {}
            if self.github_token:
                headers['Authorization'] = f'Bearer {self.github_token}'
                headers['Accept'] = 'application/vnd.github.v3+json'
            
            self.session = aiohttp.ClientSession(
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            )
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

class MergeSafePRAction(GitHubAction):
    """Merge pull requests that are considered safe"""
    
    def is_safe(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if PR merge is safe"""
        
        # Must have PR data
        if 'pr_number' not in data or 'repository' not in data:
            return False, "Missing PR or repository information"
        
        # Check for safe PR patterns
        pr_title = data.get('pr_title', '').lower()
        safe_keywords = ['typo', 'readme', 'docs', 'documentation', 'comment', 'test']
        
        if not any(keyword in pr_title for keyword in safe_keywords):
            return False, "PR title doesn't match safe patterns"
        
        # Must be mergeable
        if not data.get('mergeable', False):
            return False, "PR is not mergeable"
        
        # Must not be draft
        if data.get('draft', False):
            return False, "PR is still a draft"
        
        return True, "Safe to merge"
    
    async def execute(self, data: Dict[str, Any]) -> ActionResult:
        """Merge a safe pull request"""
        
        try:
            await self._ensure_session()
            
            repository = data['repository']
            pr_number = data['pr_number']
            
            # Double-check safety
            safe, reason = self.is_safe(data)
            if not safe:
                return ActionResult(False, error=f"Safety check failed: {reason}")
            
            # Merge the PR
            url = f"https://api.github.com/repos/{repository}/pulls/{pr_number}/merge"
            merge_data = {
                'commit_title': f"Merge PR #{pr_number}: {data.get('pr_title', 'Auto-merge')}",
                'merge_method': 'merge'
            }
            
            async with self.session.put(url, json=merge_data) as response:
                if response.status == 200:
                    result_data = await response.json()
                    
                    self.execution_count += 1
                    self.last_execution = datetime.utcnow()
                    
                    return ActionResult(True, {
                        'pr_number': pr_number,
                        'repository': repository,
                        'merged': True,
                        'sha': result_data.get('sha'),
                        'message': result_data.get('message', 'Merged successfully')
                    })
                else:
                    error_data = await response.json()
                    return ActionResult(False, error=f"GitHub API error: {error_data.get('message', 'Unknown error')}")
        
        except Exception as e:
            logger.error(f"Merge PR action failed: {e}")
            return ActionResult(False, error=str(e))

class UpdateDependenciesAction(BaseAction):
    """Update package dependencies safely"""
    
    def get_requirements(self) -> List[str]:
        return ['git', 'package manager (npm/pip/uv)']
    
    def is_safe(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if dependency update is safe"""
        
        # Only update security-related dependencies automatically
        if not data.get('security_updates', False):
            return False, "Only security updates are auto-approved"
        
        # Must have package information
        if not data.get('packages'):
            return False, "No packages specified for update"
        
        return True, "Safe security update"
    
    async def execute(self, data: Dict[str, Any]) -> ActionResult:
        """Update dependencies using appropriate package manager"""
        
        try:
            packages = data.get('packages', [])
            project_path = data.get('project_path', '.')
            
            # Detect package manager
            project_dir = Path(project_path)
            
            if (project_dir / 'package.json').exists():
                # Node.js project
                return await self._update_npm_packages(project_dir, packages)
            elif (project_dir / 'pyproject.toml').exists():
                # Python project with UV
                return await self._update_python_packages_uv(project_dir, packages)
            elif (project_dir / 'requirements.txt').exists():
                # Python project with pip
                return await self._update_python_packages_pip(project_dir, packages)
            else:
                return ActionResult(False, error="No supported package manager detected")
        
        except Exception as e:
            logger.error(f"Update dependencies action failed: {e}")
            return ActionResult(False, error=str(e))
    
    async def _update_npm_packages(self, project_dir: Path, packages: List[str]) -> ActionResult:
        """Update npm packages"""
        
        try:
            # Create backup of package.json
            backup_file = project_dir / 'package.json.backup'
            shutil.copy2(project_dir / 'package.json', backup_file)
            
            # Update packages
            cmd = ['npm', 'update'] + packages if packages else ['npm', 'update']
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=project_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return ActionResult(True, {
                    'package_manager': 'npm',
                    'packages_updated': packages,
                    'stdout': stdout.decode(),
                    'backup_created': str(backup_file)
                })
            else:
                return ActionResult(False, error=f"npm update failed: {stderr.decode()}")
        
        except Exception as e:
            return ActionResult(False, error=f"npm update error: {e}")
    
    async def _update_python_packages_uv(self, project_dir: Path, packages: List[str]) -> ActionResult:
        """Update Python packages using UV"""
        
        try:
            # Update packages with UV
            if packages:
                # Update specific packages
                for package in packages:
                    cmd = ['uv', 'add', f'{package}@latest']
                    
                    process = await asyncio.create_subprocess_exec(
                        *cmd,
                        cwd=project_dir,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    
                    await process.communicate()
                    
                    if process.returncode != 0:
                        return ActionResult(False, error=f"Failed to update {package}")
            else:
                # Sync all dependencies
                cmd = ['uv', 'sync', '--upgrade']
                
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    cwd=project_dir,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    return ActionResult(False, error=f"uv sync failed: {stderr.decode()}")
            
            return ActionResult(True, {
                'package_manager': 'uv',
                'packages_updated': packages,
                'action': 'sync --upgrade' if not packages else 'add @latest'
            })
        
        except Exception as e:
            return ActionResult(False, error=f"UV update error: {e}")
    
    async def _update_python_packages_pip(self, project_dir: Path, packages: List[str]) -> ActionResult:
        """Update Python packages using pip"""
        
        try:
            if packages:
                # Update specific packages
                cmd = ['pip', 'install', '--upgrade'] + packages
            else:
                # Update from requirements.txt
                cmd = ['pip', 'install', '--upgrade', '-r', 'requirements.txt']
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=project_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return ActionResult(True, {
                    'package_manager': 'pip',
                    'packages_updated': packages,
                    'stdout': stdout.decode()
                })
            else:
                return ActionResult(False, error=f"pip update failed: {stderr.decode()}")
        
        except Exception as e:
            return ActionResult(False, error=f"pip update error: {e}")

class FormatCodeAction(BaseAction):
    """Format code using appropriate formatters"""
    
    def get_requirements(self) -> List[str]:
        return ['git', 'code formatters (black/prettier/etc)']
    
    async def execute(self, data: Dict[str, Any]) -> ActionResult:
        """Format code files"""
        
        try:
            files = data.get('files', [])
            project_path = data.get('project_path', '.')
            
            project_dir = Path(project_path)
            formatted_files = []
            
            # Detect file types and format accordingly
            python_files = [f for f in files if f.endswith('.py')]
            js_files = [f for f in files if f.endswith(('.js', '.ts', '.jsx', '.tsx'))]
            
            # Format Python files with black
            if python_files:
                result = await self._format_python_files(project_dir, python_files)
                if result.success:
                    formatted_files.extend(python_files)
            
            # Format JavaScript/TypeScript files with prettier
            if js_files:
                result = await self._format_js_files(project_dir, js_files)
                if result.success:
                    formatted_files.extend(js_files)
            
            return ActionResult(True, {
                'formatted_files': formatted_files,
                'total_files': len(formatted_files)
            })
        
        except Exception as e:
            logger.error(f"Format code action failed: {e}")
            return ActionResult(False, error=str(e))
    
    async def _format_python_files(self, project_dir: Path, files: List[str]) -> ActionResult:
        """Format Python files with black"""
        
        try:
            cmd = ['black'] + files
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=project_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return ActionResult(True, {'formatter': 'black', 'output': stdout.decode()})
            else:
                return ActionResult(False, error=f"Black formatting failed: {stderr.decode()}")
        
        except Exception as e:
            return ActionResult(False, error=f"Black formatter error: {e}")
    
    async def _format_js_files(self, project_dir: Path, files: List[str]) -> ActionResult:
        """Format JavaScript/TypeScript files with prettier"""
        
        try:
            cmd = ['prettier', '--write'] + files
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=project_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return ActionResult(True, {'formatter': 'prettier', 'output': stdout.decode()})
            else:
                return ActionResult(False, error=f"Prettier formatting failed: {stderr.decode()}")
        
        except Exception as e:
            return ActionResult(False, error=f"Prettier formatter error: {e}")

class BackupConfigAction(BaseAction):
    """Create backup of configuration files"""
    
    async def execute(self, data: Dict[str, Any]) -> ActionResult:
        """Create backup of configuration files"""
        
        try:
            config_files = data.get('config_files', ['.claude/'])
            backup_dir = data.get('backup_dir', 'backups')
            
            # Create backup directory with timestamp
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            backup_path = Path(backup_dir) / f'config_backup_{timestamp}'
            backup_path.mkdir(parents=True, exist_ok=True)
            
            backed_up_files = []
            
            for config_file in config_files:
                source_path = Path(config_file)
                
                if source_path.exists():
                    if source_path.is_file():
                        # Copy single file
                        dest_path = backup_path / source_path.name
                        shutil.copy2(source_path, dest_path)
                        backed_up_files.append(str(source_path))
                    elif source_path.is_dir():
                        # Copy entire directory
                        dest_path = backup_path / source_path.name
                        shutil.copytree(source_path, dest_path)
                        backed_up_files.append(str(source_path))
            
            return ActionResult(True, {
                'backup_path': str(backup_path),
                'backed_up_files': backed_up_files,
                'total_files': len(backed_up_files)
            })
        
        except Exception as e:
            logger.error(f"Backup config action failed: {e}")
            return ActionResult(False, error=str(e))

class CreateIssueAction(GitHubAction):
    """Create GitHub issues for tracked problems"""
    
    def is_safe(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if issue creation is safe"""
        
        if 'repository' not in data or 'issue_title' not in data:
            return False, "Missing repository or issue title"
        
        # Avoid spam - check if similar issue might already exist
        title = data['issue_title'].lower()
        if len(title) < 10:
            return False, "Issue title too short"
        
        return True, "Safe to create issue"
    
    async def execute(self, data: Dict[str, Any]) -> ActionResult:
        """Create a GitHub issue"""
        
        try:
            await self._ensure_session()
            
            repository = data['repository']
            title = data['issue_title']
            body = data.get('issue_body', '')
            labels = data.get('labels', [])
            
            # Create issue
            url = f"https://api.github.com/repos/{repository}/issues"
            issue_data = {
                'title': title,
                'body': body,
                'labels': labels
            }
            
            async with self.session.post(url, json=issue_data) as response:
                if response.status == 201:
                    issue_result = await response.json()
                    
                    return ActionResult(True, {
                        'issue_number': issue_result['number'],
                        'issue_url': issue_result['html_url'],
                        'repository': repository,
                        'title': title
                    })
                else:
                    error_data = await response.json()
                    return ActionResult(False, error=f"GitHub API error: {error_data.get('message')}")
        
        except Exception as e:
            logger.error(f"Create issue action failed: {e}")
            return ActionResult(False, error=str(e))

class ActionExecutor:
    """Main executor for autonomous actions with safety guardrails"""
    
    def __init__(self, action_config: Dict[str, Any], rep_validator = None):
        self.config = action_config
        self.rep_validator = rep_validator
        self.actions = {}
        self.enabled = action_config.get('enabled', True)
        self.max_actions_per_hour = action_config.get('max_actions_per_hour', 5)
        
        # Rate limiting
        self.execution_history = []
        
        # Auto-approve and require-confirmation lists
        self.auto_approve = set(action_config.get('auto_approve', []))
        self.require_confirmation = set(action_config.get('require_confirmation', []))
        
        # Initialize actions
        self._initialize_actions()
        
        logger.info(f"Action executor initialized with {len(self.actions)} actions")
    
    def _initialize_actions(self):
        """Initialize all available actions"""
        
        # GitHub actions
        github_config = self.config.get('github', {})
        self.actions['merge_safe_pr'] = MergeSafePRAction('merge_safe_pr', github_config)
        self.actions['create_issue'] = CreateIssueAction('create_issue', github_config)
        
        # Development actions
        self.actions['update_dependencies'] = UpdateDependenciesAction('update_dependencies', {})
        self.actions['format_code'] = FormatCodeAction('format_code', {})
        self.actions['backup_config'] = BackupConfigAction('backup_config', {})
    
    def _check_rate_limit(self) -> Tuple[bool, str]:
        """Check if we're within execution rate limits"""
        
        now = datetime.utcnow()
        one_hour_ago = now - timedelta(hours=1)
        
        # Count executions in the last hour
        recent_executions = [
            execution for execution in self.execution_history
            if execution['timestamp'] > one_hour_ago and execution['success']
        ]
        
        if len(recent_executions) >= self.max_actions_per_hour:
            return False, f"Rate limit exceeded: {len(recent_executions)}/{self.max_actions_per_hour} actions in last hour"
        
        return True, "Within rate limits"
    
    async def execute(self, action_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an autonomous action with safety checks"""
        
        start_time = datetime.utcnow()
        
        try:
            # Check if executor is enabled
            if not self.enabled:
                return {
                    'success': False,
                    'error': 'Action executor is disabled',
                    'action_type': action_type,
                    'timestamp': start_time.isoformat()
                }
            
            # Check rate limits
            within_limits, limit_reason = self._check_rate_limit()
            if not within_limits:
                return {
                    'success': False,
                    'error': limit_reason,
                    'action_type': action_type,
                    'timestamp': start_time.isoformat()
                }
            
            # Check if action exists
            if action_type not in self.actions:
                return {
                    'success': False,
                    'error': f'Unknown action type: {action_type}',
                    'action_type': action_type,
                    'available_actions': list(self.actions.keys()),
                    'timestamp': start_time.isoformat()
                }
            
            action = self.actions[action_type]
            
            # Safety check
            safe, safety_reason = action.is_safe(data)
            if not safe:
                return {
                    'success': False,
                    'error': f'Safety check failed: {safety_reason}',
                    'action_type': action_type,
                    'timestamp': start_time.isoformat()
                }
            
            # Check approval requirements
            if action_type in self.require_confirmation:
                return {
                    'success': False,
                    'error': 'Action requires human confirmation',
                    'action_type': action_type,
                    'requires_confirmation': True,
                    'timestamp': start_time.isoformat()
                }
            
            # Execute the action
            logger.info(f"Executing autonomous action: {action_type}")
            result = await action.execute(data)
            
            # Record execution
            execution_record = {
                'action_type': action_type,
                'success': result.success,
                'timestamp': start_time,
                'duration_ms': (datetime.utcnow() - start_time).total_seconds() * 1000,
                'error': result.error
            }
            self.execution_history.append(execution_record)
            
            # Build response
            response = result.to_dict()
            response['action_type'] = action_type
            
            if result.success:
                logger.info(f"Action {action_type} completed successfully")
            else:
                logger.warning(f"Action {action_type} failed: {result.error}")
            
            return response
        
        except Exception as e:
            logger.error(f"Action executor error for {action_type}: {e}")
            
            # Record failed execution
            execution_record = {
                'action_type': action_type,
                'success': False,
                'timestamp': start_time,
                'duration_ms': (datetime.utcnow() - start_time).total_seconds() * 1000,
                'error': str(e)
            }
            self.execution_history.append(execution_record)
            
            return {
                'success': False,
                'error': f'Execution error: {str(e)}',
                'action_type': action_type,
                'timestamp': start_time.isoformat()
            }
    
    async def dry_run(self, action_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a dry run of an action"""
        
        if action_type not in self.actions:
            return {
                'success': False,
                'error': f'Unknown action type: {action_type}',
                'dry_run': True
            }
        
        action = self.actions[action_type]
        result = await action.dry_run(data)
        
        response = result.to_dict()
        response['action_type'] = action_type
        response['dry_run'] = True
        
        return response
    
    def get_available_actions(self) -> List[Dict[str, Any]]:
        """Get list of available actions with metadata"""
        
        actions_info = []
        
        for action_type, action in self.actions.items():
            info = {
                'name': action_type,
                'requires_confirmation': action_type in self.require_confirmation,
                'auto_approve': action_type in self.auto_approve,
                'requirements': action.get_requirements(),
                'execution_count': action.execution_count,
                'last_execution': action.last_execution.isoformat() if action.last_execution else None
            }
            actions_info.append(info)
        
        return actions_info
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get execution statistics"""
        
        now = datetime.utcnow()
        one_hour_ago = now - timedelta(hours=1)
        one_day_ago = now - timedelta(days=1)
        
        # Filter executions by time
        hour_executions = [e for e in self.execution_history if e['timestamp'] > one_hour_ago]
        day_executions = [e for e in self.execution_history if e['timestamp'] > one_day_ago]
        
        return {
            'enabled': self.enabled,
            'total_actions_available': len(self.actions),
            'rate_limit': {
                'max_per_hour': self.max_actions_per_hour,
                'executions_last_hour': len(hour_executions),
                'successful_last_hour': len([e for e in hour_executions if e['success']])
            },
            'executions': {
                'last_hour': len(hour_executions),
                'last_day': len(day_executions),
                'total_all_time': len(self.execution_history)
            },
            'success_rates': {
                'last_hour': len([e for e in hour_executions if e['success']]) / max(len(hour_executions), 1),
                'last_day': len([e for e in day_executions if e['success']]) / max(len(day_executions), 1)
            }
        }
    
    async def close(self):
        """Close action executor and cleanup resources"""
        
        # Close GitHub actions
        for action in self.actions.values():
            if hasattr(action, 'close'):
                await action.close()
        
        logger.info("Action executor closed")

# Testing
async def test_action_executor():
    """Test action executor functionality"""
    
    print("🤖 Testing PADA Action Executor")
    print("=" * 50)
    
    # Test configuration
    test_config = {
        'enabled': True,
        'max_actions_per_hour': 10,
        'auto_approve': ['format_code', 'backup_config'],
        'require_confirmation': ['merge_safe_pr', 'update_dependencies'],
        'github': {
            'token': None  # Add token for real testing
        }
    }
    
    # Initialize executor
    executor = ActionExecutor(test_config)
    
    try:
        # Test backup action (safe)
        backup_data = {
            'config_files': ['test_file.txt'],
            'backup_dir': 'test_backups'
        }
        
        # Create test file
        with open('test_file.txt', 'w') as f:
            f.write('test content')
        
        result = await executor.execute('backup_config', backup_data)
        
        if result['success']:
            print("✅ Backup action test passed")
        else:
            print(f"❌ Backup action test failed: {result['error']}")
        
        # Get statistics
        stats = executor.get_statistics()
        print(f"📊 Actions executed: {stats['executions']['total_all_time']}")
        
        # Clean up test files
        import os
        import shutil
        if os.path.exists('test_file.txt'):
            os.remove('test_file.txt')
        if os.path.exists('test_backups'):
            shutil.rmtree('test_backups')
        
        # Close executor
        await executor.close()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        await executor.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_action_executor())