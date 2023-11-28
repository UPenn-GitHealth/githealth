import Image from 'next/image'

// import { useSession } from 'next-auth/client'

export default function Home() {
  return (

     <div className="container">
      <main>
        <h1 className="title">
          Welcome to <a href="
          ">GitHealth</a>
        </h1>

        <div className="grid">
          <a href="/pulls_per_repo" className="card">
          " className="card">
            <h3>Pulls Per Repo &rarr;</h3>
            <p>Graph of pulls per repo</p>
          </a>

          <a href="/open_pulls_per_repo" className="card">
            <h3>Open Pulls Per Repo &rarr;</h3>
            <p>Graph of open pulls per repo</p>
          </a>

          <a href="/pulls_per_month" className="card">
            <h3>Pulls Per Month &rarr;</h3>
            <p>Graph of pulls per month</p>

          </a>

          <a href="/rolling_avg_days_to_merge" className="card">
            <h3>Rolling Avg Days to Merge &rarr;</h3>
            <p>Graph of rolling avg days to merge</p>
          </a>
        </div>
      </main>

    </div>



  )
}
