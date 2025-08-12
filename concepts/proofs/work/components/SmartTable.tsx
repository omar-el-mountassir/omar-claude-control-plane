import * as React from "react";
type Row = { id: string; title?: string; status?: string; [k: string]: any };
export default function SmartTable({ title, rows = [] }: { title: string; rows: Row[] }) {
  return (
    <div>
      <h3 style={{ margin: 0 }}>{title}</h3>
      <table><tbody>{rows.map(r => (
        <tr key={r.id}><td>{r.id}</td><td>{r.title}</td><td>{r.status}</td></tr>
      ))}</tbody></table>
    </div>
  );
}