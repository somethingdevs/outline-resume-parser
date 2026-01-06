import axios from "axios";

const client = axios.create({
  baseURL: "", // vite proxy handles it
  timeout: 600000,
});

export async function health() {
  const res = await client.get("/health");
  return res.data;
}

export async function parseResume({ file, debug }) {
  const fd = new FormData();
  fd.append("file", file);
  fd.append("debug", String(!!debug));

  const res = await client.post("/parse", fd, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function matchResume({ file, jdText, debug }) {
  const fd = new FormData();
  fd.append("file", file);
  if (jdText && jdText.trim().length > 0) fd.append("jd_text", jdText);
  fd.append("debug", String(!!debug));

  const res = await client.post("/match", fd, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}
