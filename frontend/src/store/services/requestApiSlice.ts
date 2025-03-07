import { IRequest } from "@/src/lib/types";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const requestApiSlice = createApi({
    reducerPath: "requestApi",
    baseQuery: fetchBaseQuery({
        baseUrl: "https://prod-team-30-mdmsvlv5.final.prodcontest.ru/api/request",
    }),
    tagTypes: ["Stats"],
    endpoints: (build) => ({
        getRequestsByMentorId: build.query<IRequest[], IRequest["mentor_id"]>({
            query: (mentorId) => ({
                url: `/mentor/${mentorId}`,
            }),
            providesTags: ["Stats"],
        }),
        getRequestsByStudentId: build.query<IRequest[], IRequest["student_id"]>({
            query: (studentId) => ({
                url: `/student/${studentId}`,
            }),
            providesTags: ["Stats"],
        }),
        createRequest: build.mutation<
            { request_id: IRequest["request_id"] },
            {
                mentor_id: IRequest["mentor_id"];
                student_id: IRequest["student_id"];
                query: IRequest["query"];
                status: IRequest["query"];
                date: IRequest["date"];
            }
        >({
            query: (body) => ({
                url: "",
                body,
                method: "POST",
            }),
        }),
        editRequest: build.mutation<
            {
                mentor_id: IRequest["mentor_id"];
                student_id: IRequest["student_id"];
                query: IRequest["query"];
                status: IRequest["query"];
                date: IRequest["date"];
            },
            {
                status?: IRequest["status"];
                query?: IRequest["query"];
                date?: IRequest["date"];
                request_id: IRequest["request_id"];
            }
        >({
            query: ({ status, query, request_id, date }) => ({
                url: `/${request_id}`,
                body: {
                    status,
                    query,
                    date,
                },
                method: "PATCH",
            }),
        }),
    }),
});
