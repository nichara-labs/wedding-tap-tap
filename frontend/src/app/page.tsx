"use client";

import { toast } from "sonner";
import { settings } from "@/lib/settings";

type TapType = "bride" | "groom";

const sendTap = async (type: TapType) => {
  const resp = await fetch(`${settings.api_base_url}/${type}`, {
    method: "POST",
  });
  if (!resp.ok) {
    throw new Error(`Failed to record ${type} tap`);
  }
};

export default function TapPage() {
  const handleTap = (type: TapType) => {
    const label = type === "bride" ? "Bride" : "Groom";
    toast.promise(sendTap(type), {
      loading: `Recording ${label} tap...`,
      success: `${label} +1`,
      error: "Failed to record tap",
    });
  };

  return (
    <main className="min-h-screen w-full grid grid-rows-2 md:grid-rows-1 md:grid-cols-2 text-white">
      <button
        type="button"
        onClick={() => handleTap("bride")}
        className="w-full h-full flex items-center justify-center text-5xl md:text-7xl font-extrabold tracking-wide bg-linear-to-br from-pink-500 via-rose-500 to-fuchsia-500 active:scale-[0.99] transition"
      >
        Bride
      </button>
      <button
        type="button"
        onClick={() => handleTap("groom")}
        className="w-full h-full flex items-center justify-center text-5xl md:text-7xl font-extrabold tracking-wide bg-linear-to-br from-purple-600 via-violet-600 to-fuchsia-600 active:scale-[0.99] transition"
      >
        Groom
      </button>
    </main>
  );
}
