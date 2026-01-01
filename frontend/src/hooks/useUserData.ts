import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/client";

export const useUserData = () => {
  const userQuery = api.queryOptions("get", "/v1/auth/me");
  return useQuery({
    ...userQuery,
    queryFn: async (ctx) => {
      // We need to use a new AbortSignal for each query
      const signal = AbortSignal.timeout(3000);
      return await userQuery.queryFn({ ...ctx, signal });
    },
    retry: (failureCount, error) =>
      error.status_code !== 401 && failureCount < 3,
  });
};
