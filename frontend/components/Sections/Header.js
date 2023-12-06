import { RefreshIcon, CloseIcon } from "../Icons";

export const Header = ({ config, refreshChat, closeChat }) => {
  const headerStyle = {
    backgroundColor: 'rgb(255, 255, 255)',
    color: 'rgb(238, 17, 71)',
  };

  const headerColorStyle = {
    color: config["header-font-color"],
  };

  return (
    <div className="sai-chatbox-header" style={headerStyle}>
      <div
        className="sai-chatbox-title current-chatbot-name"
        // contentEditable="true"
      >
        {'WishartGroup'}
      </div>
      <div className="sai-btns">
        <button
          type="button"
          className="btn icon-only refresh-chat"
          data-tippy-content="Refresh chat"
          onClick={refreshChat}
          style={headerColorStyle}
        >
          <RefreshIcon />
        </button>
        <button
          type="button"
          className="btn icon-only close-chat"
          data-tippy-content="Close chat"
          onClick={closeChat}
          style={headerColorStyle}
        >
          <CloseIcon />
        </button>
      </div>
    </div>
  );
};
