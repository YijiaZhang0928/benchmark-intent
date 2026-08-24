import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://deepalign-bench-report.sanfordzhang.chatgpt.site"),
  title: "Ask or Infer?｜任务特异的个性化评测",
  description: "研究、编码与数据分析 agent 的主动偏好获取、history 推断与交付物个性化评测",
  openGraph: {
    title: "Ask or Infer?｜任务特异的个性化评测",
    description: "区分 Ask、natural-history Infer 与 PDR full-persona bridge；测量 δ 校准和最终交付物特异性。",
    images: [{ url: "/AskInfer-Bench_评测框架_v0.60.png", width: 3200, height: 1800, alt: "AskInfer-Bench v0.60 评测框架" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Ask or Infer?｜任务特异的个性化评测",
    description: "主动获取偏好、history 推断与交付物个性化。",
    images: ["/AskInfer-Bench_评测框架_v0.60.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="zh-CN"><body>{children}</body></html>;
}
