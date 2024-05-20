import { useMemo } from "react";
import { warnings } from "../assets/dummyWarnings";
import Header from "./Header";

export default function WarningList() {

  const warningList = useMemo(() => {
    return warnings;
  }, []);

  const renderWarningLists = warningList.map((w,i) => {
    return (
      <tr key={i}>
        <td>{w.warningText}</td>
        <td>{w.detail}</td>
      </tr>
    );
  })

  return (
  <>
  <Header />
    <main>
        <h1 className="warning-title">경고 리스트</h1>
        <div>
          <table className="warning-table">
            <thead>
              <tr>
                <th>단계</th>
                <th>내용</th>
              </tr>
            </thead>
            <tbody>
              {renderWarningLists}
            </tbody>
          </table>
        </div>
    </main>
  </>
  )
}
