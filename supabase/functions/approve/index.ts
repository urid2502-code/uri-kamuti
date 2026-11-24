// Used by approve.html (the link in the owner's e-mail).
// POST {id, t}            -> who is asking to join and whether already approved
// POST {id, t, approve:1} -> approve the account
// The per-account secret token (members.token) is the authorization; it only appears in the e-mail.
import { createClient } from "npm:@supabase/supabase-js@2.49.4";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "method" }, 405);
  let body: { id?: string; t?: string; approve?: unknown } = {};
  try { body = await req.json(); } catch { return json({ error: "bad" }, 400); }
  const { id, t } = body;
  if (!id || !t || !UUID.test(id) || !UUID.test(t)) return json({ error: "bad" }, 400);

  const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const { data: m } = await admin.from("members").select("user_id,email,name,approved,token").eq("user_id", id).maybeSingle();
  if (!m || m.token !== t) return json({ error: "notfound" }, 404);

  if (body.approve && !m.approved) {
    const { error } = await admin.from("members").update({ approved: true, approved_at: new Date().toISOString() }).eq("user_id", id);
    if (error) return json({ error: "db" }, 500);
    m.approved = true;
  }
  return json({ name: m.name, email: m.email, approved: m.approved });
});
