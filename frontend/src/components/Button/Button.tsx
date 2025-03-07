"use client";
import clsx from "clsx";
import { ButtonHTMLAttributes } from "react";
import styles from "./Button.module.css";

function Button({
    variant = "default",
    size = "md",
    className,
    onClick = () => {},
    children,
    ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: "default" | "alt";
    size?: "xs" | "sm" | "md" | "lg" | "xl";
} & {
    children?: React.ReactNode | undefined;
    onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
}) {
    return (
        <button
            className={clsx(
                styles.button,
                variant != "default" && styles[variant],
                styles[size],
                className,
            )}
            onClick={onClick}
            {...props}>
            {children}
        </button>
    );
}

export default Button;
