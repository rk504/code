import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Map from './components/Map'
import OpportunityList from './components/OpportunityList'
import { getOpportunities } from '../lib/data'

export default function Home() {
  const opportunities = getOpportunities()

  return (
    <div className="flex flex-col h-screen">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 flex">
          <div className="w-1/2 overflow-y-auto">
            <OpportunityList opportunities={opportunities} />
          </div>
          <div className="w-1/2">
            <Map opportunities={opportunities} />
          </div>
        </main>
      </div>
    </div>
  )
}

