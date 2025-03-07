import Header from "@/src/widgets/Header/Header";
import { ReactNode } from "react";

const Template = ({ children }: { children: ReactNode }) => {
    return (
        <div>
            <Header />
            {children}
        </div>
    );
};

export default Template;
