"use client";

import { sendGTMEvent } from "@next/third-parties/google";
import { useCallback, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/client";

const emailPattern = /.+@.+\..+/;

type FormState = "idle" | "loading" | "success" | "error";

export const SubscribeForm = () => {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<FormState>("idle");
  const [error, setError] = useState<string | null>(null);
  const emailMutation = api.useMutation("post", "/v1/email/subscribe");

  const submitDisabled = useMemo(() => {
    return status === "loading" || !emailPattern.test(email.trim());
  }, [email, status]);

  const onSubmit = useCallback(
    async (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      sendGTMEvent({ event: "subscribe" });

      if (submitDisabled) {
        return;
      }

      const trimmedEmail = email.trim();
      setStatus("loading");
      setError(null);

      emailMutation.mutate(
        { params: { query: { email: trimmedEmail } } },
        {
          onSuccess: () => {
            setStatus("success");
            setEmail("");
          },
          onError: (_err) => {
            setStatus("error");
            setError("We hit an unexpected error, please try again");
          },
        },
      );
    },
    [email, emailMutation, submitDisabled],
  );

  if (status === "success") {
    return (
      <div className="flex flex-col items-center justify-center gap-2 rounded-2xl border border-white/10 bg-white/5 p-6 text-center backdrop-blur-xl">
        <h3 className="text-lg font-semibold text-white">
          You're on the list!
        </h3>
        <p className="text-sm text-slate-300">
          Thanks! We'll reach out with launch updates and early access invites.
        </p>
      </div>
    );
  }

  return (
    <form
      onSubmit={onSubmit}
      className="relative flex flex-col gap-3 rounded-2xl border border-white/10 bg-white/5 p-4 text-left backdrop-blur-xl sm:flex-row sm:items-center sm:gap-2 sm:p-2"
    >
      <div className="flex-1">
        <label htmlFor="launch-email" className="sr-only">
          Email address
        </label>
        <Input
          id="launch-email"
          type="email"
          required
          placeholder="Enter your email"
          value={email}
          onChange={(event) => {
            setEmail(event.target.value);
          }}
          aria-invalid={status === "error"}
          aria-describedby="launch-email-hint"
          className="h-12 rounded-xl border-white/20 bg-[#0c0720]/70 text-base text-white placeholder:text-slate-400"
        />
      </div>
      <Button
        type="submit"
        size="lg"
        className="h-12 min-w-40 rounded-xl bg-violet-500 shadow-[0_18px_50px_-20px_rgba(148,113,255,0.8)] hover:bg-violet-400"
        disabled={submitDisabled}
      >
        {status === "loading" ? "Joining..." : "Join the Launch List"}
      </Button>
      <p
        id="launch-email-hint"
        className="text-xs text-slate-300 sm:absolute sm:-bottom-9 sm:left-4"
      >
        {status === "error"
          ? (error ?? "We could not save your email.")
          : "No spam—just launch updates and early access invites."}
      </p>
    </form>
  );
};
