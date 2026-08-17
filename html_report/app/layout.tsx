import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://deepalign-bench-report.sanfordzhang.chatgpt.site"),
  title: "DeepAlign-Bench｜真人真值、CDM 与 D-JQS",
  description: "三个长程知识工作场景中的反事实用户特异性评测与人类来源测量协议",
  openGraph: {
    title: "DeepAlign-Bench｜绝对适配不等于反事实用户特异性",
    description: "真人 task-conditioned ledger、Counterfactual Difference Map、受约束 rubric 与 D-JQS。",
    images: [{ url: "/DeepAlign-Bench_真人真值到D-JQS_v0.55.png", width: 3200, height: 1800, alt: "DeepAlign-Bench 真人真值到 D-JQS 流程" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "DeepAlign-Bench｜绝对适配不等于反事实用户特异性",
    description: "真人 task-conditioned ledger、Counterfactual Difference Map、受约束 rubric 与 D-JQS。",
    images: ["/DeepAlign-Bench_真人真值到D-JQS_v0.55.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="zh-CN"><body>{children}</body></html>;
}
