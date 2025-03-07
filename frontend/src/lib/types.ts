export interface IMentor {
    mentor_id: number;
    password?: string;
    name: string;
    email: string;
    expertise?: string;
    bio: string;
    score: number;
    tags: string[];
    telegram?: string;
    requests?: IRequest[];
}

export interface IStudent {
    id: string;
    password: string;
    email: string;
    name: string;
    telegram: string;
    age: number;
    bio: string;
}

export interface IStats {
    total_students: number;
    total_mentors: number;
    accepted: number;
    refused: number;
    pending: number;
}
export type IRequest = {
    request_id: string;
    mentor_id: string;
    student_id: string;
    query: string;
    status: "ACCEPTED" | "REFUSED" | "PENDING";
    date: string;
};

export interface IGetRoleResponse {
    role: "mentor" | "student";
    id: string;
}
