import { createFormHook, createFormHookContexts } from "@tanstack/react-form";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { Input as ShadcnInput } from "@/components/ui/input";
import { Textarea as ShadcnTextarea } from "@/components/ui/textarea";

const { fieldContext, formContext, useFieldContext } = createFormHookContexts();

const useFieldContext_ = <T,>() => {
  const field = useFieldContext<T>();
  const isInvalid =
    !field.state.meta.isValid &&
    (!!field.state.meta.errorMap.onSubmit || !field.state.meta.isPristine);
  return { field, isInvalid };
};

const Input = ({
  label,
  placeholder,
}: {
  label: string;
  placeholder?: string;
}) => {
  const { field, isInvalid } = useFieldContext_<string>();
  return (
    <Field data-invalid={isInvalid}>
      <FieldLabel htmlFor={field.name}>{label}</FieldLabel>
      <ShadcnInput
        id={field.name}
        name={field.name}
        value={field.state.value}
        placeholder={placeholder}
        onBlur={field.handleBlur}
        onChange={(e) => {
          field.handleChange(e.target.value);
        }}
        aria-invalid={isInvalid}
      />
      {isInvalid && <FieldError errors={field.state.meta.errorMap.onChange} />}
    </Field>
  );
};

const Textarea = ({
  label,
  placeholder,
}: {
  label: string;
  placeholder?: string;
}) => {
  const { field, isInvalid } = useFieldContext_<string>();
  return (
    <Field data-invalid={isInvalid}>
      <FieldLabel htmlFor={field.name}>{label}</FieldLabel>
      <ShadcnTextarea
        id={field.name}
        className="max-h-60 h-full"
        name={field.name}
        placeholder={placeholder}
        value={field.state.value}
        onBlur={field.handleBlur}
        onChange={(e) => field.handleChange(e.target.value)}
        aria-invalid={isInvalid}
      />
      {isInvalid && <FieldError errors={field.state.meta.errorMap.onChange} />}
    </Field>
  );
};

export const { useAppForm } = createFormHook({
  fieldContext,
  formContext,
  fieldComponents: { Input, Textarea },
  formComponents: {},
});
