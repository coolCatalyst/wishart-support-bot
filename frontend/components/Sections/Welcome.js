export const WelcomeComponent = ({config}) => {
  return (
    <div className="bot-msg">
      {config["hide-bot-avatar"] == "on" && config["hide-bot-avatar"] ? (
        <></>
      ) : (
        <div className="sai-msg-header">
          <img className="sai-msg-logo" src={config["bot-avatar"]} />
          <span className="sai-msg-name">{config.chatbot_name}</span>
        </div>
      )}
      <div className="sai-msg">
        <span className="msg-content">{config["welcome_message"]}</span>
      </div>
    </div>
  );
};
