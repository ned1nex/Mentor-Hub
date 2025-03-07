import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { userApiSlice } from "../services/userApiSlice";

interface IInitialState {
    id: string;
    role: string | null;
}

const initialState: IInitialState = {
    id: "",
    role: null,
};

export const userSlice = createSlice({
    name: "user",
    initialState,
    reducers: {
        setUser: (state, action: PayloadAction<{ id: string }>) => {
            state.id = action.payload.id;
        },
        setRole: (state, action: PayloadAction<{ role: string }>) => {
            state.role = action.payload.role;
        },
    },
    extraReducers: (builder) => {
        builder.addMatcher(
            userApiSlice.endpoints.getRoleByToken.matchFulfilled,
            (state, { payload }) => {
                if ("id" in payload && "role" in payload) {
                    state.id = payload.id;
                    state.role = payload.role;
                }
            },
        );
    },
});
export const { setRole, setUser } = userSlice.actions;
