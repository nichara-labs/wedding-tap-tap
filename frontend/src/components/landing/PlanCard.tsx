"use client";

import { ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export const PlanCard = ({
  title,
  price,
  features,
  primary = false,
  subtitle,
}: {
  title: string;
  price: string;
  features: string[];
  primary?: boolean;
  subtitle?: string;
}) => {
  return (
    <Card
      className={`relative flex flex-col overflow-hidden border-white/10 bg-white/5 backdrop-blur-xl transition-transform duration-300 hover:-translate-y-1 ${primary ? "shadow-[0_35px_90px_-50px_rgba(148,113,255,0.9)]" : "shadow-[0_25px_70px_-55px_rgba(99,102,241,0.8)]"}`}
    >
      <div className="absolute inset-0 pointer-events-none">
        <div
          className={`absolute inset-0 ${primary ? "bg-[radial-gradient(circle_at_top,_rgba(168,85,247,0.25),_transparent_65%)]" : "bg-[radial-gradient(circle_at_top,_rgba(59,130,246,0.22),_transparent_65%)]"}`}
        />
      </div>
      <CardHeader className="items-center text-center pb-4">
        <CardTitle className="font-headline text-2xl">{title}</CardTitle>
        <div className="my-2 text-4xl font-bold font-headline text-white">
          {price}
        </div>
        <CardDescription className="text-slate-200">
          {subtitle ??
            (primary ? "For legendary campaigns" : "For curious adventurers")}
        </CardDescription>
      </CardHeader>
      <CardContent className="flex-grow">
        <ul className="space-y-3">
          {features.map((feature) => (
            <li key={feature} className="flex items-center gap-3">
              <ShieldCheck className="h-5 w-5 text-violet-200" />
              <span className="text-slate-200">{feature}</span>
            </li>
          ))}
        </ul>
      </CardContent>

      <div className="p-6 pt-0">
        <Button
          className={`group relative w-full cursor-pointer overflow-hidden ${primary ? "bg-violet-500 text-white hover:bg-violet-500/90" : "border border-white/30 bg-white/10 text-white hover:bg-white/20"}`}
          variant={primary ? "default" : "secondary"}
        >
          {/* Glint/shimmer overlay */}
          <span
            aria-hidden="true"
            className="group-hover:animate-glint absolute inset-y-0 left-0 w-[60%] -skew-x-12 group-hover:bg-gradient-to-r from-transparent via-white/40 to-transparent"
          />
          <span className="relative z-10 inline-flex items-center justify-center">
            Coming soon!
          </span>
        </Button>
      </div>
    </Card>
  );
};
