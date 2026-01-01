import { PanelLeftIcon } from "lucide-react";
import Link from "next/link";
import { useCallback } from "react";
import { Logo } from "@/components/common/Logo";
import { Button } from "@/components/ui/button";
import { useSidebar } from "@/components/ui/sidebar";
import { cn } from "@/lib/utils";

export const LogoButton = ({
  ...props
}: React.ComponentPropsWithoutRef<typeof Button>) => {
  const { open, setOpen, setOpenMobile } = useSidebar();

  const onClick = useCallback(
    (e: React.MouseEvent) => {
      if (open) {
        setOpenMobile(false);
        return; // Allow clicks to passthrough when open
      }
      setOpen(true);
      e.preventDefault(); // block navigation when opening sidebar
    },
    [open, setOpen, setOpenMobile],
  );
  return (
    <Button asChild variant="ghost" size="icon" onClick={onClick} {...props}>
      <Link
        href="/game"
        className={cn("flex justify-between", !open && "cursor-e-resize")}
      >
        <Logo
          className={cn("size-7", !open && "group-hover/sidebar:hidden")}
          aria-hidden
        />
        <PanelLeftIcon
          className={cn("hidden", !open && "group-hover/sidebar:block")}
          aria-hidden
        />
      </Link>
    </Button>
  );
};
