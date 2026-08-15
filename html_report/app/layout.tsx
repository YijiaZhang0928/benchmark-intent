import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://deepalign-bench-report.sanfordzhang.chatgpt.site"),
  title: "DeepAlign-Bench｜三个长程知识工作场景",
  description: "PLHKW 任务资源池与反事实用户特异性评测",
  openGraph: {
    title: "DeepAlign-Bench｜绝对适配不等于反事实用户特异性",
    description: "180 候选、60 provisional 与三个代表性长程知识工作场景。",
    images: [{ url: "/DeepAlign-Bench_PLHKW任务资源池_v0.54.png", width: 3200, height: 1800, alt: "DeepAlign-Bench PLHKW 任务资源池与升级门" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "DeepAlign-Bench｜绝对适配不等于反事实用户特异性",
    description: "180 候选、60 provisional 与三个代表性长程知识工作场景。",
    images: ["/DeepAlign-Bench_PLHKW任务资源池_v0.54.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="zh-CN"><body>{children}</body></html>;
}
