function Settings() {
  return (
    <div className="mx-auto max-w-4xl space-y-8">
      <div>
        <h1 className="text-2xl font-semibold">Settings</h1>
        <p className="mt-2 text-sm text-zinc-500">
          Configure your Nsight workspace.
        </p>
      </div>

      <section className="rounded-xl border border-zinc-200 bg-white">
        <div className="border-b border-zinc-200 px-5 py-4">
          <h2 className="font-semibold">General</h2>
        </div>

        <div className="space-y-6 p-5">
          <div>
            <label className="text-sm font-medium">Workspace name</label>

            <input
              defaultValue="My Nsight Workspace"
              className="mt-2 w-full rounded-lg border border-zinc-200 px-3 py-2.5 text-sm outline-none focus:border-zinc-500"
            />
          </div>

          <div>
            <label className="text-sm font-medium">Default language</label>

            <select
              defaultValue="en"
              className="mt-2 w-full rounded-lg border border-zinc-200 px-3 py-2.5 text-sm outline-none"
            >
              <option value="en">English</option>
              <option value="fr">French</option>
            </select>
          </div>
        </div>
      </section>

      <section className="rounded-xl border border-zinc-200 bg-white">
        <div className="border-b border-zinc-200 px-5 py-4">
          <h2 className="font-semibold">AI Provider</h2>
        </div>

        <div className="p-5">
          <p className="text-sm leading-6 text-zinc-500">
            AI provider configuration will be added when the backend AI
            pipeline is implemented.
          </p>
        </div>
      </section>
    </div>
  );
}

export default Settings;