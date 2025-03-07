import { IStudent } from "@/src/lib/types";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const studentApiSlice = createApi({
    reducerPath: "studentApi",
    baseQuery: fetchBaseQuery({
        baseUrl: "https://prod-team-30-mdmsvlv5.final.prodcontest.ru/api/students",
    }),
    tagTypes: ["Student"],
    endpoints: (build) => ({
        check: build.query<{ newToken: string } | { message: string }, string>({
            query: (token) => ({
                url: "/students/auth",
                headers: {
                    authorization: token,
                },
            }),
        }),
        getStudent: build.query<IStudent, string>({
            query: (id) => ({
                url: `/${id}`,
            }),
            providesTags: ["Student"],
        }),
        signup: build.mutation<
            { token: string },
            {
                email: IStudent["email"];
                password: IStudent["password"];
                name: IStudent["name"];
                telegram?: IStudent["telegram"];
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
            { email: IStudent["email"]; password: IStudent["password"] }
        >({
            query: (body) => ({
                url: `/sign-in`,
                method: "POST",
                body,
            }),
        }),
        updateUser: build.mutation<
            IStudent,
            {
                id: IStudent["id"];
                name?: IStudent["name"];
                age?: IStudent["age"];
                bio?: IStudent["bio"];
                telegram?: IStudent["telegram"];
            }
        >({
            query: (student) => ({
                url: `/students/${student.id}`,
                method: "PUT",
                body: student,
            }),
        }),
    }),
});
