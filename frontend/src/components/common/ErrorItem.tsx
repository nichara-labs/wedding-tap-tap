import { AlertCircleIcon, RotateCcw } from "lucide-react";
import type { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

import { Button } from "../ui/button";
import { ItemActions } from "../ui/item";
import { Spinner } from "../ui/spinner";

type Props = (
  | {
      message: string;
      refetch: () => void;
      isFetching: boolean;
    }
  | {
      message: string;
      refetch?: never;
      isFetching?: never;
    }
) &
  HTMLAttributes<HTMLDivElement>;

export const ErrorItem = (props: Props) => {
  const { message, className, refetch, isFetching, ...divProps } = props;

  return (
    <div
      className={cn(
        "max-w-full flex items-center gap-4 rounded-md border p-4 text-sm text-destructive/80",
        className,
      )}
      {...divProps}
    >
      <AlertCircleIcon className="shrink-0" />
      <span className="truncate" title={message}>
        {message}
      </span>
      {refetch && (
        <ItemActions>
          <Button
            disabled={Boolean(isFetching)}
            onClick={refetch}
            variant="outline"
          >
            {isFetching ? <Spinner /> : <RotateCcw />}
            Retry
          </Button>
        </ItemActions>
      )}
    </div>
  );
};
