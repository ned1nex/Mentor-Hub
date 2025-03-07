import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { IGetRoleResponse } from "@/src/lib/types";

export const userApiSlice = createApi({
    reducerPath: "userApi",
    baseQuery: fetchBaseQuery({
        baseUrl: "https://prod-team-30-mdmsvlv5.final.prodcontest.ru/api",
    }),
    endpoints: (build) => ({
        getRoleByToken: build.query<IGetRoleResponse, string>({
            query: (token) => ({
                url: "/get-role",
                method: "GET",
                headers: {
                    authorization: `Bearer ${token}`,
                },
            }),
        }),
        getRoleById: build.query<IGetRoleResponse, number>({
            query: (instanceId) => `/get-role/${instanceId}`,
        }),
    }),
});

export const {
    useGetRoleByTokenQuery,
    useLazyGetRoleByTokenQuery,
    useGetRoleByIdQuery,
    useLazyGetRoleByIdQuery,
} = userApiSlice;
