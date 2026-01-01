import { useTheme } from "next-themes";
import type React from "react";
import type { RefObject } from "react";
import Markdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import {
  oneDark,
  oneLight,
} from "react-syntax-highlighter/dist/esm/styles/prism";
import remarkGfm from "remark-gfm";
import { cn } from "@/lib/utils";

type Props = {
  messageRole: "user" | "assistant" | "system";
  content: string;
  ref?: RefObject<HTMLDivElement | null>;
};

export const ChatMessageBubble = ({ messageRole, content, ref }: Props) => {
  const { resolvedTheme } = useTheme();

  const render = (
    <div className="prose prose-lg dark:prose-invert max-w-none prose-hr:my-[1.5em] prose-code:before:hidden prose-code:after:hidden">
      {content ? (
        <Markdown
          remarkPlugins={[remarkGfm]}
          components={{
            pre: ({ children }) => children,
            code(props) {
              const { children, className, ...rest } = props;
              const match = /language-(\w+)/.exec(className || "");
              return match ? (
                <SyntaxHighlighter
                  PreTag={"div"}
                  language={match[1]}
                  style={resolvedTheme === "dark" ? oneDark : oneLight}
                  codeTagProps={{ className: "font-mono text-sm" }}
                >
                  {String(children).replace(/\n$/, "")}
                </SyntaxHighlighter>
              ) : (
                <code {...rest} className={cn("font-mono", className)}>
                  {children}
                </code>
              );
            },
          }}
        >
          {content}
        </Markdown>
      ) : (
        <span className="italic opacity-70">(empty message)</span>
      )}
    </div>
  );

  switch (messageRole) {
    case "assistant":
      return (
        <AssistantMessageContainer ref={ref}>
          {render}
        </AssistantMessageContainer>
      );
    case "user":
      return <UserMessageContainer ref={ref}>{render}</UserMessageContainer>;
    default: // Don't show system messages
      return;
  }
};

const UserMessageContainer = ({
  children,
  ref,
}: React.PropsWithChildren & { ref?: RefObject<HTMLDivElement | null> }) => (
  <div className="flex justify-end my-2" ref={ref}>
    <div className=" bg-secondary text-secondary-foreground max-w-10/12 rounded-2xl px-4 py-3 shadow-md">
      {children}
    </div>
  </div>
);

const AssistantMessageContainer = ({
  children,
  ref,
}: React.PropsWithChildren & { ref?: RefObject<HTMLDivElement | null> }) => (
  <div className="my-2" ref={ref}>
    {children}
  </div>
);
