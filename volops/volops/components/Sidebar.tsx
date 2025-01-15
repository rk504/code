import { Slider } from '@/components/ui/slider'
import { Checkbox } from '@/components/ui/checkbox'

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 p-6 overflow-y-auto">
      <h2 className="text-lg font-semibold mb-4">Filters</h2>
      
      <div className="mb-6">
        <h3 className="text-sm font-medium mb-2">Distance</h3>
        <Slider defaultValue={[50]} max={100} step={1} />
        <div className="flex justify-between text-sm text-gray-500 mt-1">
          <span>0 km</span>
          <span>100 km</span>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-sm font-medium mb-2">Categories</h3>
        <div className="space-y-2">
          {['Education', 'Environment', 'Health', 'Community', 'Animals'].map((category) => (
            <div key={category} className="flex items-center">
              <Checkbox id={category} />
              <label htmlFor={category} className="ml-2 text-sm text-gray-700">{category}</label>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-sm font-medium mb-2">Availability</h3>
        <div className="space-y-2">
          {['Weekdays', 'Weekends', 'Morning', 'Afternoon', 'Evening'].map((time) => (
            <div key={time} className="flex items-center">
              <Checkbox id={time} />
              <label htmlFor={time} className="ml-2 text-sm text-gray-700">{time}</label>
            </div>
          ))}
        </div>
      </div>
    </aside>
  )
}

