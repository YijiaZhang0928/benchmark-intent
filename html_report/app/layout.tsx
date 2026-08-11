import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://elicitalign-bench-report.sanfordzhang.chatgpt.site"),
  title: "ElicitAlign-Bench｜自然欠指定任务中的用户状态发现与利用",
  description: "正式研究 Proposal 的可读 HTML 汇报版",
  openGraph: {
    title: "ElicitAlign-Bench｜从缺失用户信息到个性化交付",
    description: "评测 agent 是否会自主发现、澄清、停止并利用会改变最终建议的用户信息。",
    images: [{ url: "/ElicitAlign-Bench_端到端流程图_v0.45.png", width: 3200, height: 1800, alt: "ElicitAlign-Bench 端到端评测流程" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "ElicitAlign-Bench｜从缺失用户信息到个性化交付",
    description: "评测 agent 是否会自主发现、澄清、停止并利用会改变最终建议的用户信息。",
    images: ["/ElicitAlign-Bench_端到端流程图_v0.45.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="zh-CN"><body>{children}</body></html>;
}
