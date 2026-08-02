import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://deepalign-bench-report.sanfordzhang.chatgpt.site"),
  title: "DeepAlign-Bench｜长程 Deep Research 个性化评测",
  description: "正式研究 Proposal 的可读 HTML 汇报版",
  openGraph: {
    title: "DeepAlign-Bench｜长程 Deep Research 个性化评测",
    description: "用反事实用户对评估最终交付物是否真正适合目标用户。",
    images: [{ url: "/og.png", width: 1672, height: 941, alt: "DeepAlign-Bench 反事实个性化评测流程" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "DeepAlign-Bench｜长程 Deep Research 个性化评测",
    description: "用反事实用户对评估最终交付物是否真正适合目标用户。",
    images: ["/og.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="zh-CN"><body>{children}</body></html>;
}
