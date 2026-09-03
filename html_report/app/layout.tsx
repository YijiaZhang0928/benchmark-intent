import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://deepalign-bench-report.sanfordzhang.chatgpt.site"),
  title: "Ask or Infer?｜任务特异的个性化评测",
  description: "研究、编码与数据分析 agent 的主动偏好获取、history 推断与交付物个性化评测",
  openGraph: {
    title: "Ask or Infer?｜任务特异的个性化评测",
    description: "从 PDR 50 题按个性化诊断价值筛到 15 题，再区分 Ask、natural-history Infer 与 full-persona bridge。",
    images: [{ url: "/AskInfer-Bench_评测框架_v0.61.png", width: 3200, height: 1800, alt: "AskInfer-Bench v0.61 评测框架" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Ask or Infer?｜任务特异的个性化评测",
    description: "PDR 50→15、主动获取偏好、history 推断与交付物个性化。",
    images: ["/AskInfer-Bench_评测框架_v0.61.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="zh-CN"><body>{children}</body></html>;
}
