import Avatar from "@/src/components/Avatar/Avatar";
import Badge from "@/src/components/Badge/Badge";
import Button from "@/src/components/Button/Button";
import Container from "@/src/components/Container/Container";
import TextWithIcon from "@/src/components/TextWithIcon/TextWithIcon";
import { IoMdCloud, IoMdMail } from "react-icons/io";
import { RiTelegram2Fill } from "react-icons/ri";
import styles from "./ProfileInfo.module.css";

interface ProfileInfoProps {
    email: string;
    username: string;
    tg: string;
    isMentor?: boolean;
    xp?: number;
}

function ProfileInfo({ isMentor = false, xp = 0, username, email, tg }: ProfileInfoProps) {
    return (
        <Container>
            <Avatar abbreviation={username.substring(0, 1)} size={80} />
            <div className={styles.info}>
                <div className={styles.username}>
                    {username} {isMentor && <Badge>{xp} XP</Badge>}
                </div>
                <TextWithIcon style={{ color: "var(--fg-alt)" }}>
                    <IoMdMail /> {email}
                </TextWithIcon>
                <TextWithIcon style={{ color: "var(--fg-alt)" }}>
                    <RiTelegram2Fill /> @{tg}
                </TextWithIcon>
                <Button size="xs" variant="alt">
                    <IoMdCloud /> Загрузить аватар...
                </Button>
            </div>
        </Container>
    );
}

export default ProfileInfo;
