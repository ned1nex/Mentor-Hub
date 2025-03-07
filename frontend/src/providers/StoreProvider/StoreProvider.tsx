"use client";
import { getToken } from "@/src/lib/jwt";
import { userApiSlice } from "@/src/store/services/userApiSlice";
import { AppStore, setupStore } from "@/src/store/store";
import { ReactNode, useRef } from "react";
import { Provider } from "react-redux";

export default function StoreProvider({ children }: { children: ReactNode }) {
    const storeRef = useRef<AppStore | null>(null);
    if (!storeRef.current) {
        storeRef.current = setupStore();
        storeRef.current.dispatch(userApiSlice.endpoints.getRoleByToken.initiate(getToken() || ""));
    }

    return <Provider store={storeRef.current}>{children}</Provider>;
}
