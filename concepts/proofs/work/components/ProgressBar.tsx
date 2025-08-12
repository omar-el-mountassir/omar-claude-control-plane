import * as React from "react";
export default function ProgressBar({ value = 0, label = "Progress" }: { value?: number; label?: string }) {
  const v = Math.max(0, Math.min(100, Number(value) || 0));
  return (
    <div style={{ width: "100%" }}>
      <div style={{ fontSize: 12 }}>{label}: {v}%</div>
      <div style={{ height: 8, background: "#eee" }}>
        <div style={{ width: v + "%", height: 8 }} />
      </div>
    </div>
  );
}