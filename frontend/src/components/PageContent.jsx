import { Outlet } from "react-router";

import { Layout, theme, Button } from "antd";

import {FormOutlined} from "@ant-design/icons";

import { CreateModal, useModalContext, useModalDataContext } from "./ModalProvider.jsx";

const { Content } = Layout;


export function PageContent({ header, children }) {
    const {token: { colorBgContainer, borderRadiusLG }} = theme.useToken();
    const contentStyle = {
        padding: 10,
        background: colorBgContainer,
        borderRadius: borderRadiusLG,
    };
    const [modalOpen, setModalOpen] = useModalContext();
    const [modalData, setModalData] = useModalDataContext();

    return (
        <Content className="mx-2 mt-3">
            <div style={contentStyle} className="h-full">
                <div className="flex flex-row items-center">
                    <span className="text-xl">{header}</span>
                    <Button
                        className="items-baseline"
                        title="Create new"
                        type="button"
                        icon={<FormOutlined />}
                        onClick={() => setModalOpen({visible: true, modalId: 1})}
                        size="small"
                    />
                </div>

                <div className="mt-3">
                    {children}
                </div>

                <CreateModal modalId={1} />
                <CreateModal modalId={2} data={modalData} />
            </div>
        </Content>
    );
}
