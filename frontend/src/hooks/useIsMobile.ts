"use client";

import { useClientMediaQuery } from "./useClientMediaQuery";

export function useIsMobile() {
    return useClientMediaQuery("(max-width: 768px)");
}
