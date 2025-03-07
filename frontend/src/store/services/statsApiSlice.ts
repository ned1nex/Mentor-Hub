import { IStats } from "@/src/lib/types";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const statsApiSlice = createApi({
    reducerPath: "statsApi",
    baseQuery: fetchBaseQuery({
        baseUrl: "https://prod-team-30-mdmsvlv5.final.prodcontest.ru/api",
    }),
    tagTypes: ["Stats"],
    endpoints: (build) => ({
        getStats: build.query<IStats, null>({
            query: () => ({
                url: `/stats`,
            }),
            providesTags: ["Stats"],
        }),
    }),
});
