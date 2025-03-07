import { clsx } from "clsx";
import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import StoreProvider from "../providers/StoreProvider/StoreProvider";
import "./globals.css";

const sansSerif = Montserrat({
    variable: "--font-sans-serif",
    subsets: ["latin"],
});

export const metadata: Metadata = {
    title: "MentorHub",
    description: "Платформа для поиска менторов",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <StoreProvider>
            <html lang="ru">
                <body className={clsx(sansSerif.className)}>{children}</body>
            </html>
        </StoreProvider>
    );
}
