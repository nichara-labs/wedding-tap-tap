"use client";

import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { settings } from "@/lib/settings";

export default function ResetPage() {
  const onClick = async () => {
    const resp = await fetch(`${settings.api_base_url}/reset`, {
      method: "POST",
    });
    if (!resp.ok) {
      toast.error("Failed to reset");
      return;
    }
    toast.success("Resetted counts");
  };
  return <Button onClick={onClick}>Reset counts</Button>;
}
