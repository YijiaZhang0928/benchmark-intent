import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://deepalign-bench-report.sanfordzhang.chatgpt.site"),
  title: "DeepAlign-Bench｜个性化研究交付物的下游决策效用评测",
  description: "正式研究 Proposal 的可读 HTML 汇报版",
  openGraph: {
    title: "DeepAlign-Bench｜个性化研究交付物的下游决策效用评测",
    description: "用真实目标用户、随机化报告处理与可验证决定评估个性化研究交付物的下游效用。",
    images: [{ url: "/og.png", width: 1672, height: 941, alt: "DeepAlign-Bench 两阶段下游决策效用评测流程" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "DeepAlign-Bench｜个性化研究交付物的下游决策效用评测",
    description: "用真实目标用户、随机化报告处理与可验证决定评估个性化研究交付物的下游效用。",
    images: ["/og.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="zh-CN"><body>{children}</body></html>;
}
