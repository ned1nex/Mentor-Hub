import { combineSlices, configureStore } from "@reduxjs/toolkit";
import { mentorApiSlice } from "./services/mentorApiSlice";
import { studentApiSlice } from "./services/studentApiSlice";
import { statsApiSlice } from "./services/statsApiSlice";
import { userApiSlice } from "./services/userApiSlice";
import { userSlice } from "./reducers/userSlice";
import { requestApiSlice } from "./services/requestApiSlice";
import { adminApiSlice } from "./services/adminApiSlice";

const rootReducer = combineSlices(
    mentorApiSlice,
    studentApiSlice,
    statsApiSlice,
    userApiSlice,
    userSlice,
    requestApiSlice,
    adminApiSlice,
);

export const setupStore = () => {
    return configureStore({
        reducer: rootReducer,
        middleware: (getDefaultMiddleware) => {
            return getDefaultMiddleware().concat(
                mentorApiSlice.middleware,
                studentApiSlice.middleware,
                statsApiSlice.middleware,
                userApiSlice.middleware,
                requestApiSlice.middleware,
                adminApiSlice.middleware,
            );
        },
    });
};

export type RootState = ReturnType<typeof rootReducer>;
export type AppStore = ReturnType<typeof setupStore>;
export type AppDispatch = AppStore["dispatch"];
