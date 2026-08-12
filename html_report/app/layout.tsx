import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://deepalign-bench-report.sanfordzhang.chatgpt.site"),
  title: "DeepAlign-Bench｜反事实用户特异性评测",
  description: "正式研究 Proposal 的可读 HTML 汇报版",
  openGraph: {
    title: "DeepAlign-Bench｜绝对适配不等于反事实用户特异性",
    description: "用 paired-user 交叉矩阵与非补偿 profile 评测个性化 Deep Research。",
    images: [{ url: "/DeepAlign-Bench_整体框架与PDR压力测试_v0.48.png", width: 3200, height: 1800, alt: "DeepAlign-Bench 整体评测框架" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "DeepAlign-Bench｜绝对适配不等于反事实用户特异性",
    description: "用 paired-user 交叉矩阵与非补偿 profile 评测个性化 Deep Research。",
    images: ["/DeepAlign-Bench_整体框架与PDR压力测试_v0.48.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="zh-CN"><body>{children}</body></html>;
}
