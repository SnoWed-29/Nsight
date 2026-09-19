import { Navigate, Route, Routes } from "react-router-dom";

import AppLayout from "./components/layout/AppLayout";

import Dashboard from "./pages/Dashboard";
import Datasets from "./pages/Datasets";
import DatasetOverview from "./pages/DatasetOverview";
import DataExplorer from "./pages/DataExplorer";
import Schema from "./pages/Schema";
import Relationships from "./pages/Relationships";
import AskNsight from "./pages/AskNsight";
import SQL from "./pages/SQL";
import Settings from "./pages/Settings";

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />

        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/datasets" element={<Datasets />} />

        <Route path="/datasets/:datasetId" element={<DatasetOverview />} />
        <Route path="/datasets/:datasetId/data" element={<DataExplorer />} />
        <Route path="/datasets/:datasetId/schema" element={<Schema />} />
        <Route
          path="/datasets/:datasetId/relationships"
          element={<Relationships />}
        />

        <Route path="/ask" element={<AskNsight />} />
        <Route path="/sql" element={<SQL />} />

        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}

export default App;