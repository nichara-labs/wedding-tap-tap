"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect } from "react";
import { toast } from "sonner";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { FieldGroup } from "@/components/ui/field";
import { useAppForm } from "@/hooks/useAppForm";
import { api } from "@/lib/client";
import { STORY_PARAM } from "@/lib/constants";
import { useStore } from "@/lib/store";

const RequiredString = z.string().trim().min(1, "Can't be empty");

const formSchema = z.object({
  description: RequiredString,
  prompt: RequiredString,
  title: RequiredString,
});

export const CreateView = () => {
  const searchParams = useSearchParams();
  const storyId = searchParams.get(STORY_PARAM) || null;
  const story = api.useQuery(
    "get",
    "/v1/stories/{story_id}",
    {
      params: { path: { story_id: storyId || "" } },
    },
    { enabled: !!storyId },
  );
  const isEditing = !!story.data;
  const setHeaderText = useStore((s) => s.setHeaderText);
  const router = useRouter();
  const { mutate: createStory } = api.useMutation("post", "/v1/stories", {
    onError: () => toast.error("Failed to create story"),
    onSuccess: () => router.push("/game"),
  });
  const { mutate: editStory } = api.useMutation(
    "put",
    "/v1/stories/{story_id}",
    {
      onError: () => toast.error("Failed to edit story"),
      onSuccess: () => {
        toast.success("Successfully edited story", {
          position: "bottom-right",
        });
        router.push("/game");
      },
    },
  );
  const { mutate: deleteStory } = api.useMutation(
    "delete",
    "/v1/stories/{story_id}",
    {
      onError: () => toast.error("Failed to delete story"),
      onSuccess: () => {
        toast.success("Deleted story", {
          position: "bottom-right",
        });
        router.push("/game");
      },
    },
  );

  const form = useAppForm({
    defaultValues: {
      title: "",
      description: "",
      prompt: "",
    },
    validators: {
      onSubmit: formSchema,
      onChange: formSchema,
    },
    onSubmit: ({ value }) => {
      if (isEditing)
        editStory({
          body: value,
          params: { path: { story_id: story.data.id } },
        });
      else createStory({ body: value });
    },
  });

  useEffect(() => {
    setHeaderText(storyId ? "Edit Story" : "Write Your Story");
  }, [setHeaderText, storyId]);

  useEffect(() => {
    if (story.error) {
      toast.error("Failed to fetch story");
      return;
    } else if (story.isPending || !("prompt" in story.data)) {
      return;
    }

    form.setFieldValue("title", story.data.title);
    form.setFieldValue("description", story.data.description);
    form.setFieldValue("prompt", story.data.prompt);
  }, [story, form]);

  return (
    <div className="max-w-3xl mx-auto flex flex-col my-2">
      <Card className="flex-1">
        <CardHeader>
          <CardTitle>Write Your Story</CardTitle>
          <CardDescription></CardDescription>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              e.stopPropagation();
            }}
          >
            <FieldGroup>
              <form.AppField name="title">
                {(field) => <field.Input label="Title" />}
              </form.AppField>

              <form.AppField name="description">
                {(field) => (
                  <field.Input
                    label="Description"
                    placeholder="A short sentence to describe the story"
                  />
                )}
              </form.AppField>

              <form.AppField name="prompt">
                {(field) => (
                  <field.Textarea
                    label="Prompt"
                    placeholder="An outline of how the story should unfold"
                  />
                )}
              </form.AppField>
            </FieldGroup>
          </form>
        </CardContent>
        <CardFooter className="gap-2 justify-between">
          {isEditing ? (
            <Button
              onClick={() =>
                deleteStory({ params: { path: { story_id: story.data.id } } })
              }
              variant={"destructive"}
            >
              Delete Story
            </Button>
          ) : (
            <Button onClick={() => void form.reset()} variant={"destructive"}>
              Reset
            </Button>
          )}
          <Button onClick={() => void form.handleSubmit()}>
            {isEditing ? "Edit " : "Create "}Story
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};
