import { ArrowDown } from "lucide-react";
import React, { type RefObject, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type Props = React.ComponentPropsWithoutRef<typeof Button> & {
  targetRef: RefObject<HTMLElement | null>;
};

export const ScrollUntilElement = ({
  targetRef,
  className,
  ...props
}: Props) => {
  const [visible, setVisible] = useState(false);

  const scrollToBottom = () => {
    if (!targetRef.current) return;
    targetRef.current.scrollIntoView({ block: "end", inline: "nearest" });
  };

  useEffect(() => {
    if (!targetRef.current) return;
    const cb = (entries: IntersectionObserverEntry[]) => {
      // Show button only if element begins to appear
      setVisible(entries.some((e) => !e.isIntersecting));
    };
    const observer = new IntersectionObserver(cb, {
      root: null,
      threshold: 0,
    });
    observer.observe(targetRef.current);
    return () => observer.disconnect();
  }, [targetRef]);

  return (
    <Button
      size="icon"
      variant={"default"}
      onClick={scrollToBottom}
      className={cn(!visible && "invisible", className)}
      {...props}
    >
      <ArrowDown />
    </Button>
  );
};
