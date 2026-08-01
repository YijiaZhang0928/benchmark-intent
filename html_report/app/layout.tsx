import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DeepAlign-Bench｜长程 Deep Research 个性化评测",
  description: "正式研究 Proposal 的可读 HTML 汇报版",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="zh-CN"><body>{children}</body></html>;
}
