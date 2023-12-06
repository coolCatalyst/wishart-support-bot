import { diff_time } from "../utils";
import { botMSGStyle } from "../../components/Styles";

export const MainComponent = ({ datas, config }) => {
  const userMSGStyle = {
    backgroundColor: config["user-chat-bubble-background-color"],
  };
  return (
    <>
      {datas.map((data, index) => {
        let hide_sources = "off";
        if (
          config["hide-sources"] !== undefined &&
          config["hide-sources"] === "on"
        ) {
          hide_sources = "on";
        }
        return (
          <div
            key={index}
            className={data.type == "bot" ? "bot-msg" : "user-msg"}
          >
            {config["hide-bot-avatar"] === "on" && config["hide-bot-avatar"] ? (
              <></>
            ) : (
              data.type === "bot" && (
                <div className="sai-msg-header">
                  <img
                    className="sai-msg-logo"
                    src='/img/wishart.png'
                    alt="Bot Avatar"
                  />
                  <span className="sai-msg-name">{config.chatbot_name}</span>
                </div>
              )
            )}
            <div
              className="sai-msg"
              style={data.type == "bot" ? botMSGStyle : userMSGStyle}
            >
              <span className="msg-content">{data.message}</span>
            </div>

            {data.type === "bot" &&
            data.source !== "" &&
            data.source !== undefined &&
            hide_sources==='off' ? (
              <div className="sai-sources">
                {data.source.split(",").map((source, index) => {
                  return (
                    <div key={index}>
                      <a href="#" className="primary-color" target="_blank">
                        {source}
                      </a>
                    </div>
                  );
                })}
              </div>
            ) : (
              <></>
            )}
            {diff_time(data.date)}
          </div>
        );
      })}
    </>
  );
};
