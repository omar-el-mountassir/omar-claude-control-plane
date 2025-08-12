import * as React from "react";
type Progress = { focusScore?: number; velocity?: { weekly?: number; unit?: string }; updatedAt?: string };
export default function SessionState({ progress = {} as Progress }: { progress?: Progress }) {
  const v = progress.velocity || {};
  return (
    <div style={{ fontSize: 12 }}>
      <div>Velocity: {v.weekly ?? "?"} {v.unit ?? ""}</div>
      <div>Updated: {progress.updatedAt ?? "?"}</div>
    </div>
  );
}