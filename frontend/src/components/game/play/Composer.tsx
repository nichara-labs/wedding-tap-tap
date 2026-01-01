import { ArrowUp, Square } from "lucide-react";
import type { KeyboardEvent } from "react";
import TextareaAutosize, {
  type TextareaAutosizeProps,
} from "react-textarea-autosize";
import { Button } from "@/components/ui/button";
import { useIsMobile } from "@/hooks/use-mobile";
import { cn } from "@/lib/utils";

type Props = {
  onSubmit: (text: string) => unknown;
  state: "ready" | "streaming";
  handleAbort: () => unknown;
  text: string;
  setText: (text: string) => unknown;
} & Omit<TextareaAutosizeProps, "onSubmit">;

export const Composer = ({
  className,
  state,
  onSubmit,
  handleAbort,
  text,
  setText,
  ...props
}: Props) => {
  const isMobile = useIsMobile();

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (state === "streaming" || text.trim() === "") return;

    // 'Enter' only works on the desktop
    if (!isMobile && e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSubmit(text);
      setText("");
    }
  };

  const handleClick = () => {
    if (state === "ready") {
      onSubmit(text);
      setText("");
    } else {
      handleAbort();
    }
  };

  const buttonDisabled = state === "ready" && text.trim() === "";

  return (
    <form className={cn("relative bg-background", className)}>
      <TextareaAutosize
        value={text}
        onChange={(e) => setText(e.target.value)}
        maxRows={5}
        className={cn(
          `
          flex field-sizing-content w-full resize-none pl-3 pr-14 py-4 rounded-md border border-input bg-background dark:bg-input/30

          text-base placeholder:text-muted-foreground

          shadow-xs outline-none transition-[color,box-shadow]

          disabled:cursor-not-allowed disabled:opacity-50
        `,
        )}
        onKeyDown={handleKeyDown}
        {...props}
      />
      <Button
        type="button"
        size="icon"
        className="absolute w-10 h-10 bottom-2 right-2"
        disabled={buttonDisabled}
        onClick={handleClick}
      >
        {state === "ready" ? <ArrowUp className="size-5" /> : <Square />}
      </Button>
    </form>
  );
};
