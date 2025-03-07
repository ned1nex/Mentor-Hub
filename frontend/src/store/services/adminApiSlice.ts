import { IStudent } from "@/src/lib/types";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const adminApiSlice = createApi({
    reducerPath: "adminApi",
    baseQuery: fetchBaseQuery({
        baseUrl: "https://prod-team-30-mdmsvlv5.final.prodcontest.ru/api/admin",
    }),
    endpoints: (build) => ({
        login: build.mutation<
            { token: string },
            { email: IStudent["email"]; password: IStudent["password"] }
        >({
            query: (body) => ({
                url: `/sign-in`,
                method: "POST",
                body,
            }),
        }),
    }),
});
