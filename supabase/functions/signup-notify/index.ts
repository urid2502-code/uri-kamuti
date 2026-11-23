// Called by the site (auth.js) when a signed-in user is not approved yet.
// Sends the site owner one e-mail per new account, with a button that opens approve.html.
// Requires the secret RESEND_API_KEY (Resend account registered with the owner's e-mail).
import { createClient } from "npm:@supabase/supabase-js@2.49.4";

const OWNER = "urid2502@gmail.com";
const SITE = "https://urid2502-code.github.io/uri-kamuti/";
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });
const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "method" }, 405);

  const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const jwt = (req.headers.get("Authorization") || "").replace(/^Bearer\s+/i, "");
  const { data: u, error: ue } = await admin.auth.getUser(jwt);
  if (ue || !u?.user) return json({ error: "auth" }, 401);
  const user = u.user;

  let { data: m } = await admin.from("members").select("*").eq("user_id", user.id).maybeSingle();
  if (!m) {
    const meta = user.user_metadata || {};
    const ins = await admin.from("members")
      .insert({ user_id: user.id, email: user.email, name: meta.full_name || meta.name || "" })
      .select("*").single();
    m = ins.data;
  }
  if (!m) return json({ error: "db" }, 500);
  if (m.approved) return json({ status: "approved" });
  if (m.notified_at) return json({ status: "pending" });

  const key = Deno.env.get("RESEND_API_KEY");
  if (!key) return json({ status: "pending", mail: "not-configured" });

  const link = `${SITE}approve.html?id=${m.user_id}&t=${m.token}`;
  const name = esc(m.name || "(ללא שם)"), email = esc(m.email || "");
  const html = `<div dir="rtl" style="font-family:Arial,sans-serif;max-width:480px;margin:auto;padding:24px;color:#0F172A">
<h2 style="margin:0 0 12px">הרשמה חדשה ל־urIQ</h2>
<p style="margin:0 0 4px"><b>${name}</b></p>
<p style="margin:0 0 20px;color:#475569" dir="ltr" align="right">${email}</p>
<a href="${link}" style="display:inline-block;background:#12805C;color:#fff;text-decoration:none;font-weight:bold;padding:12px 26px;border-radius:10px">לאישור המשתמש</a>
<p style="margin:22px 0 0;color:#64748B;font-size:13px">הכפתור פותח את דף האישור באתר. עד שתאשר/י, המשתמש לא יוכל לפתור מקבצים.</p></div>`;

  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: "urIQ <onboarding@resend.dev>",
      to: [OWNER],
      subject: `הרשמה חדשה ל־urIQ: ${m.name || m.email}`,
      html,
    }),
  });
  if (!r.ok) return json({ status: "pending", mail: "failed", detail: await r.text() });
  await admin.from("members").update({ notified_at: new Date().toISOString() }).eq("user_id", m.user_id);
  return json({ status: "pending", mail: "sent" });
});
