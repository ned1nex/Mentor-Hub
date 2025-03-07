"use client";
import DropdownMenu from "@/src/components/DropdownMenu/DropdownMenu";
import { useIsMobile } from "@/src/hooks/useIsMobile";
import { clearToken } from "@/src/lib/jwt";
import { useAppSelector } from "@/src/store/hooks";
import { mentorApiSlice } from "@/src/store/services/mentorApiSlice";
import { studentApiSlice } from "@/src/store/services/studentApiSlice";
import Avatar from "../../components/Avatar/Avatar";
import styles from "./Header.module.css";
import Logo from "./Logo/Logo";
import NavLink from "./NavLink/NavLink";

function Header() {
    const isMobile = useIsMobile();
    const role = useAppSelector((state) => state.user.role);
    const userId = useAppSelector((state) => state.user.id);
    const { data } =
        role == "student"
            ? studentApiSlice.useGetStudentQuery(userId)
            : mentorApiSlice.useGetMentorByIdQuery(userId);

    return (
        <header className={styles.header}>
            {!isMobile && (
                <NavLink asChild href="/">
                    <Logo />
                </NavLink>
            )}

            <nav className={styles.nav}>
                {role === "student" && <NavLink href="/">Поиск</NavLink>}
                {!role ? (
                    <NavLink href="/login">Вход</NavLink>
                ) : (
                    <DropdownMenu
                        items={[
                            { label: "Профиль", href: "/profile" },
                            {
                                label: "Мои заявки",
                                href: role == "mentor" ? "/mentor" : "/requests",
                            },
                            { label: "Выход", href: "/login", onClick: () => clearToken() },
                        ]}
                        trigger={<Avatar abbreviation={data?.name.slice(0, 1) || "!"} />}
                        links
                    />
                )}
            </nav>
        </header>
    );
}

export default Header;
