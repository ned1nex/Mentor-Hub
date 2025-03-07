import { IMentor } from "@/src/lib/types";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export interface IGetMentorsResponse {
    mentor: IMentor;
    score: number;
    text: string;
}

export const mentorApiSlice = createApi({
    reducerPath: "mentorApi",
    baseQuery: fetchBaseQuery({
        baseUrl: `https://prod-team-30-mdmsvlv5.final.prodcontest.ru/api/mentors`,
    }),
    tagTypes: ["Mentor"],
    endpoints: (build) => ({
        getMentors: build.query<IGetMentorsResponse[], string>({
            query: (userQuery) => ({
                url: `?query=${userQuery}`,
            }),
            providesTags: ["Mentor"],
        }),
        getMentorById: build.query<IMentor, string>({
            query: (mentorId) => ({
                url: `/${mentorId}`,
            }),
        }),
        check: build.query<{ newToken: string } | { message: string }, string>({
            query: (token) => ({
                url: "/auth",
                headers: {
                    authorization: token,
                },
            }),
        }),
        signup: build.mutation<
            { token: string },
            {
                email: IMentor["email"];
                password: IMentor["password"];
                name: IMentor["name"];
                expertise: IMentor["expertise"];
                bio: IMentor["bio"];
                tags: IMentor["tags"];
                telegram?: IMentor["telegram"];
            }
        >({
            query: (body) => ({
                url: "/sign-up",
                method: "POST",
                body,
            }),
        }),
        login: build.mutation<
            { token: string },
            { email: IMentor["email"]; password: IMentor["password"] }
        >({
            query: (body) => ({
                url: `/sign-in`,
                method: "POST",
                body,
            }),
        }),
    }),
});
