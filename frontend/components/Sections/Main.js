import { diff_time } from "../utils";
import { botMSGStyle } from "../../components/Styles";
import ReactMarkdown from "react-markdown";
import Markdown from "react-markdown";
function Section({ title, content }) {
  return (
    <div>
      <p>{title}</p>
      <h3>{content}</h3>
    </div>
  );
}
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
        let sections = [];

        try {
          sections = data.message
            .split("**")
            .reduce((sections, text, index) => {
              if (index % 2 === 0) {
                sections.push({ title: text.trim(), content: "" });
              } else {
                sections[sections.length - 1].content = text.trim();
              }
              return sections;
            }, []);
        } catch (error) {
          //Handle the error case when there are no "**"
          // console.error("Parsing error", error);
          sections = [{ title: "", content: data.message }];
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
                    src="/img/wishart.png"
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
              <span className="msg-content">
                {/* {sections.map(({ title, content }, index) => (
                  <Section key={index} title={title} content={content} />
                ))} */}
                {typeof data.message == "string" ? (
                  <Markdown >{data.message}</Markdown>
                ) : (
                  <>{data.message}</>
                )}
              </span>
            </div>

            {data.type === "bot" &&
            data.source !== "" &&
            data.source !== undefined &&
            hide_sources === "off" ? (
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
