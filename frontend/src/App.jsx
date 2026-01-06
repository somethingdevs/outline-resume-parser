import React, { useMemo, useState } from "react";
import {
  Button,
  Card,
  Divider,
  Input,
  Radio,
  Space,
  Switch,
  Typography,
  Upload,
  message,
  Tag,
} from "antd";
import {
  UploadOutlined,
  CopyOutlined,
  DownloadOutlined,
  ReloadOutlined,
} from "@ant-design/icons";
import { health, matchResume, parseResume } from "./api";

const { Title, Text } = Typography;
const { TextArea } = Input;

function downloadJson(data, filename = "result.json") {
  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export default function App() {
  const [mode, setMode] = useState("parse"); // parse | match
  const [file, setFile] = useState(null);
  const [jdText, setJdText] = useState("");
  const [debug, setDebug] = useState(false);
  const [loading, setLoading] = useState(false);

  const [apiStatus, setApiStatus] = useState({ state: "unknown", last: null }); // unknown|ok|down
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const canSubmit = useMemo(() => !!file && !loading, [file, loading]);

  async function checkHealth() {
    try {
      setApiStatus((s) => ({ ...s, state: "unknown" }));
      const data = await health();
      setApiStatus({ state: "ok", last: data });
      message.success("Backend is up");
    } catch (e) {
      setApiStatus({ state: "down", last: null });
      message.error("Backend looks down (health failed)");
    }
  }

  async function run() {
    if (!file) {
      message.warning("Upload a PDF first");
      return;
    }
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const data =
        mode === "parse"
          ? await parseResume({ file, debug })
          : await matchResume({ file, jdText, debug });

      setResult(data);
      message.success(`${mode.toUpperCase()} completed`);
    } catch (e) {
      const msg = e?.response?.data
        ? JSON.stringify(e.response.data, null, 2)
        : e?.message || "Request failed";
      setError(msg);
      message.error("Request failed");
    } finally {
      setLoading(false);
    }
  }

  const statusTag = (() => {
    if (apiStatus.state === "ok") return <Tag color="green">API OK</Tag>;
    if (apiStatus.state === "down") return <Tag color="red">API DOWN</Tag>;
    return <Tag>API ?</Tag>;
  })();

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 px-4 py-6 md:px-10 md:py-10">
      <div className="mx-auto max-w-5xl space-y-6">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="space-y-1">
            <Title level={3} className="!mb-0 !text-zinc-100">
              Outline Resume Parser
            </Title>
            <Text className="!text-zinc-400">
              Fast upload → parse/match → view JSON
            </Text>
          </div>

          <Space>
            {statusTag}
            <Button icon={<ReloadOutlined />} onClick={checkHealth}>
              Check Health
            </Button>
          </Space>
        </div>

        <Divider className="!border-zinc-800" />

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <Card
            title={<span className="text-zinc-100">Request</span>}
            bordered
            className="shadow-sm"
            styles={{ body: { padding: 18 } }}
          >
            <Space direction="vertical" style={{ width: "100%" }} size="large">
              <div className="flex items-center justify-between gap-3">
                <Radio.Group
                  value={mode}
                  onChange={(e) => setMode(e.target.value)}
                >
                  <Radio.Button value="parse">Parse</Radio.Button>
                  <Radio.Button value="match">Match</Radio.Button>
                </Radio.Group>

                <div className="flex items-center gap-2">
                  <Text className="!text-zinc-200">Debug</Text>
                  <Switch checked={debug} onChange={setDebug} />
                </div>
              </div>

              <Upload
                beforeUpload={(f) => {
                  const isPdf =
                    f.type === "application/pdf" ||
                    f.name.toLowerCase().endsWith(".pdf");
                  if (!isPdf) {
                    message.error("Please upload a PDF");
                    return Upload.LIST_IGNORE;
                  }
                  setFile(f);
                  return false; // don't auto upload
                }}
                maxCount={1}
                showUploadList={true}
                onRemove={() => setFile(null)}
              >
                <Button icon={<UploadOutlined />}>Upload Resume PDF</Button>
              </Upload>

              {mode === "match" && (
                <div className="space-y-2">
                  <Text strong className="!text-zinc-200">
                    Job Description (optional)
                  </Text>
                  <TextArea
                    value={jdText}
                    onChange={(e) => setJdText(e.target.value)}
                    placeholder="Paste JD text here (optional)"
                    autoSize={{ minRows: 6, maxRows: 12 }}
                  />
                </div>
              )}

              <Button
                type="primary"
                onClick={run}
                loading={loading}
                disabled={!canSubmit}
                block
              >
                Run {mode.toUpperCase()}
              </Button>
            </Space>
          </Card>

          <Card
            title={<span className="text-zinc-100">Response</span>}
            bordered
            className="shadow-sm"
            styles={{ body: { padding: 18 } }}
          >
            <Space direction="vertical" style={{ width: "100%" }} size="large">
              {!result && !error && (
                <Text className="!text-zinc-400">
                  Upload a PDF and click Run. You’ll see JSON here.
                </Text>
              )}

              {error && (
                <div className="rounded-md bg-red-950/40 border border-red-900 p-3">
                  <Text strong className="block !text-zinc-100">
                    Error
                  </Text>
                  <pre className="mt-2 max-h-[420px] overflow-auto whitespace-pre-wrap text-xs text-zinc-100">
                    {error}
                  </pre>
                </div>
              )}

              {result && (
                <>
                  <Space>
                    <Button
                      icon={<CopyOutlined />}
                      onClick={async () => {
                        await navigator.clipboard.writeText(
                          JSON.stringify(result, null, 2)
                        );
                        message.success("Copied JSON");
                      }}
                    >
                      Copy JSON
                    </Button>
                    <Button
                      icon={<DownloadOutlined />}
                      onClick={() =>
                        downloadJson(result, `${mode}-result.json`)
                      }
                    >
                      Download JSON
                    </Button>
                  </Space>

                  <pre className="max-h-[520px] overflow-auto rounded-md bg-zinc-900/70 border border-zinc-800 p-4 text-xs text-zinc-100">
                    {JSON.stringify(result, null, 2)}
                  </pre>
                </>
              )}
            </Space>
          </Card>
        </div>

        <Divider className="!border-zinc-800" />

        <Text className="!text-zinc-500">
          Dev note: frontend calls <code>/parse</code> and <code>/match</code>{" "}
          via Vite proxy to your FastAPI on <code>127.0.0.1:8000</code>.
        </Text>
      </div>
    </div>
  );
}
